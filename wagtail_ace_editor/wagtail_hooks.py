from wagtail import hooks
from django.utils.html import format_html
from django.templatetags.static import static

@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_ace_editor/css/ace-editor-widget.css")
    )
