from django.test import TestCase, Client
from django.conf import settings
from django import forms
from os import path
import re
from wagtail_ace_editor.forms import AceEditorField
from wagtail.templatetags.wagtailcore_tags import (
    include_block,
)


FIXTURES = path.join(settings.BASE_DIR, "core/fixtures")

space_re = re.compile(r"^\s+", re.MULTILINE)


class WidgetForm(forms.Form):
    test_field = AceEditorField(
        mode="ace/mode/django",
        theme="ace/theme/wagtail",
        use_frame_preview=False,
        frame_css=[],
        frame_js=[],
        include_template_context=False,
        required=False,
    )

class WithContextWidgetForm(forms.Form):
    test_field_tpl_context = AceEditorField(
        mode="ace/mode/django",
        theme="ace/theme/wagtail",
        use_frame_preview=False,
        include_template_context=True,
        required=False,
    )

class WidgetTestCase(TestCase):

    def test_widget_rendering(self):
        form = WidgetForm()
        p = form.as_p()
        p = space_re.sub(' ', p)
        print(p)
        self.assertInHTML("""<p>
<label for="id_test_field">Test field:</label>
<div class="ace-editor-widget">
<div class="ace-editor-preview-wrapper" id="id_test_field-preview-wrapper"></div>
<div id="id_test_field-wrapper" class="ace-editor-widget-wrapper">
<textarea id="id_test_field" name="test_field" ace-editor-input cols="40"rows="10"id="id_test_field"data-controller="ace-editor"data-ace-editor-mode-value="ace/mode/django"data-ace-editor-theme-value="ace/theme/wagtail"data-ace-editor-use-frame-preview-value="False"data-ace-editor-frame-css-value="[]"data-ace-editor-frame-js-value="[]"></textarea>
<div id="id_test_field-editor"></div>
<div class="ace-editor-widget-preview-button">
<label for="id_test_field-preview-text">Preview:</label>
<input type="checkbox" id="id_test_field-preview-check">
</div>
</div>
</div>
</p>""", p)
        
    def test_to_python(self):
        original = "<p>test {{ with_context }}</p>"
        form = WidgetForm({
            "test_field": original,
        })
        self.assertTrue(form.is_valid())
        test_field = form.cleaned_data["test_field"]
        rendered = test_field.render_as_block({
            "without_context": "context value",
        })
        self.assertEqual(rendered, original)
        self.assertEqual(str(test_field), original)

        
    def test_to_python_tpl_context(self):
        original = "<p>test {{ with_context }}</p>"
        form = WithContextWidgetForm({
            "test_field_tpl_context": original,
        })
        self.assertTrue(form.is_valid())
        test_field = form.cleaned_data["test_field_tpl_context"]
        rendered = test_field.render_as_block({
            "with_context": "context value",
        })
        self.assertEqual(rendered, "<p>test context value</p>")
        self.assertEqual(str(test_field), original)

