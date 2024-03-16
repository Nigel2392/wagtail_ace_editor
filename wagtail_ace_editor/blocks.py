from wagtail import blocks
from django.utils.safestring import mark_safe
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .forms import (
    AceEditorField,
    AceEditorValue,
)

class AceEditorBlock(blocks.FieldBlock):
    def __init__(
        self,
        mode="ace/mode/django",
        theme="ace/theme/wagtail",
        include_template_context: bool  = False,
        use_frame_preview: bool         = False,
        frame_css: list[str]            = None,
        frame_js: list[str]             = None,
        clean_html: bool                = False,
        required: bool                  = True,
        help_text: str                  = None,
        validators=(),
        **kwargs,
    ):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
            "mode": mode,
            "theme": theme,
            "clean_html": clean_html,
            "use_frame_preview": use_frame_preview,
            "frame_css": frame_css or [],
            "frame_js": frame_js or [],
        }

        self.include_template_context = include_template_context

        super().__init__(**kwargs)

    @cached_property
    def field(self):
        return AceEditorField(**self.field_options)
    
    def to_python(self, value):

        if value is None:
            return None
        
        if isinstance(value, AceEditorValue):
            return value

        return AceEditorValue(
            value,
            mode=self.field_options["mode"],
            theme=self.field_options["theme"],
            clean_html=self.field_options["clean_html"],
            render_with_context=self.include_template_context,
        )
    

