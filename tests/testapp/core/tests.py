from django.test import TestCase, Client
from django.conf import settings
from django import forms
from os import path
import re
from wagtail_ace_editor.widgets import AceEditorWidget


FIXTURES = path.join(settings.BASE_DIR, "core/fixtures")

space_re = re.compile(r"^\s+", re.MULTILINE)


class WidgetForm(forms.Form):
    test_field = forms.CharField(widget=AceEditorWidget(
        mode="ace/mode/django",
        theme="ace/theme/wagtail",
    ))

class YourCustomWidgetTestCase(TestCase):

    def test_widget_rendering(self):
        form = WidgetForm()
        p = form.as_p()
        p = space_re.sub(' ', p)
        self.assertInHTML("""<p>
<label for="id_test_field">Test field:</label>
<div class="ace-editor-widget">
<div class="ace-editor-preview-wrapper" id="id_test_field-preview-wrapper"></div>
<div id="id_test_field-wrapper" class="ace-editor-widget-wrapper">
<textarea id="id_test_field" name="test_field" ace-editor-input cols="40"rows="10"required="True"id="id_test_field"data-controller="ace-editor"data-ace-editor-mode-value="ace/mode/django"data-ace-editor-theme-value="ace/theme/wagtail"data-ace-editor-use-frame-preview-value="True"data-ace-editor-frame-css-value="[&quot;/static/wagtail_ace_editor/css/ace-editor-iframe.css&quot;]"data-ace-editor-frame-js-value="[]"></textarea>
<div id="id_test_field-editor"></div>
<div class="ace-editor-widget-preview-button">
<label for="id_test_field-preview-text">Preview:</label>
<input type="checkbox" id="id_test_field-preview-check">
</div>
</div>
</div>
</p>""", p)
