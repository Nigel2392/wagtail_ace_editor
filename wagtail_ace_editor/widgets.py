from typing import Any
from django.forms import widgets
from django.templatetags.static import static
from .clean import (
    BLEACH_CLEAN_ACE_MODES,
    clean_html,
)
import json, re



_proto_re = re.compile(r'^(?:[a-z+]+:)?//', re.I)


def format_static_if_needed(value):
    if not value:
        return value
    
    if isinstance(value, str):
        
        if _proto_re.match(value):
            return value
        
        return static(value)

    return [format_static_if_needed(v) for v in value]


class AceEditorWidget(widgets.Textarea):
    template_name = "wagtail_ace_editor/ace_editor.html"

    def __init__(self, mode="ace/mode/django", theme="ace/theme/wagtail", use_frame_preview=True, frame_css=None, frame_js=None, clean_html=False, disable_preview=False, preview_checkbox_checked=True, attrs=None):
        attrs                         = attrs or {}
        self.mode                     = mode
        self.theme                    = theme
        self.disable_preview          = True
        self.preview_checkbox_checked = preview_checkbox_checked
        self.use_frame_preview        = use_frame_preview and not disable_preview
        self.frame_css                = frame_css or [
            "wagtail_ace_editor/css/ace-editor-iframe.css"
        ] if use_frame_preview else []
        self.frame_js                 = frame_js or []
        self.clean_html               = clean_html
        super().__init__(attrs=attrs)

    def format_value(self, value) -> str | None:
        value = super().format_value(value)
        if value is None:
            return ""
        return value
    
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if self.clean_html and self.mode.lower() in BLEACH_CLEAN_ACE_MODES:
            return clean_html(value)
        return value

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        mode = self.mode
        if callable(mode):
            mode = mode()

        theme = self.theme
        if callable(theme):
            theme = theme()
            
        attrs["data-controller"] = "ace-editor"
        attrs["data-ace-editor-mode-value"] = mode
        attrs["data-ace-editor-theme-value"] = theme
        attrs["data-ace-editor-use-frame-preview-value"] = self.use_frame_preview
        attrs["data-ace-editor-frame-css-value"] = json.dumps(self.build_frame_css())
        attrs["data-ace-editor-frame-js-value"] = json.dumps(self.build_frame_js())
        attrs["data-ace-editor-preview-checkbox-checked-value"] = self.preview_checkbox_checked
        return attrs
    
    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]:
        return super().get_context(name, value, attrs) | {
            "disable_preview": self.disable_preview,
        }
    
    def build_frame_css(self):
        return format_static_if_needed(self.frame_css)

    def build_frame_js(self):
        return format_static_if_needed(self.frame_js)

    class Media:
        js = [
            "wagtail_ace_editor/js/ace.js",
            "wagtail_ace_editor/js/ace-editor.js",
            "wagtail_ace_editor/js/ace-editor-controller.js"
        ]

