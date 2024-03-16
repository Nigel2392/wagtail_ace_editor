from typing import Any
from django import forms
from django.utils.safestring import mark_safe
from django.template import Template, Context

from .widgets import AceEditorWidget


class AceEditorValue(str):
    def __new__(cls, value, mode="ace/mode/django", theme="ace/theme/wagtail", clean_html=False, render_with_context=False):
        self = super().__new__(cls, value)
        self.mode = mode
        self.theme = theme
        self.clean_html = clean_html
        self.render_with_context = render_with_context
        return self
    
    def get_context(self, context = None):
        if context is None:
            context = {}
        
        return {
            "self": self,
            "mode": self.mode,
            "theme": self.theme,
            **context
        }
    
    def render_as_block(self, context=None):
        tpl = self
        if self.render_with_context:
            if context is None:
                new_context = self.get_context(context=context)
            else:
                new_context = self.get_context(context=dict(context))

            tpl = Template(tpl)
            return tpl.render(Context(new_context))

        return mark_safe(tpl)


class AceEditorField(forms.CharField):

    def __init__(self, mode="ace/mode/django", theme="ace/theme/wagtail", use_frame_preview=False, frame_css=None, frame_js=None, clean_html=False, include_template_context=False, *args, **kwargs):
        self.mode = mode
        self.theme = theme
        self.use_frame_preview = use_frame_preview
        self.frame_css = frame_css
        self.frame_js = frame_js
        self.clean_html = clean_html
        self.include_template_context = include_template_context
        self._widget = None
        super().__init__(*args, **kwargs)

    @property
    def widget(self):
        if self._widget:
            return self._widget
        
        return AceEditorWidget(
            mode=self.mode,
            theme=self.theme,
            use_frame_preview=self.use_frame_preview,
            frame_css=self.frame_css,
            frame_js=self.frame_js,
            clean_html=self.clean_html
        )
    
    def to_python(self, value: Any | None) -> Any | None:

        if value is None:
            return None
        
        if isinstance(value, AceEditorValue):
            return value

        return AceEditorValue(
            value,
            mode=self.mode,
            theme=self.theme,
            clean_html=self.clean_html,
            render_with_context=self.include_template_context
        )
    
    @widget.setter
    def widget(self, value):
        self._widget = value



    