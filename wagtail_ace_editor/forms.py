from django import forms
from .widgets import AceEditorWidget

class AceEditorField(forms.CharField):

    def __init__(self, mode="ace/mode/django", theme="ace/theme/wagtail", use_frame_preview=False, frame_css=None, frame_js=None, clean_html=False, *args, **kwargs):
        self.mode = mode
        self.theme = theme
        self.use_frame_preview = use_frame_preview
        self.frame_css = frame_css
        self.frame_js = frame_js
        self.clean_html = clean_html
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
    
    @widget.setter
    def widget(self, value):
        self._widget = value



    