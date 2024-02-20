from django.conf import settings

from . import util

BLEACH_CLEAN_ACE_MODES = getattr(settings, "BLEACH_CLEAN_ACE_MODES", [
    "ace/mode/html",
    "ace/mode/django",
])
ALLOWED_HTML_TAGS = getattr(settings, "ALLOWED_HTML_TAGS", [tag for tag in util.HTML_TAGS if tag not in ('style', 'script')])
CLEANER_KWARGS = getattr(settings, "CLEANER_KWARGS", {
    "attributes": [
        "href",
        "src",
        "class",
        "style",
        "alt",
        "title",
        "width",
        "height",
        "id",
        "data",
    ],
    "strip": True,
    "strip_comments": True,
    "protocols": util.ALLOWED_PROTOCOLS,
})

try:
    from bleach.sanitizer import Cleaner

    _cleaner = Cleaner(tags=ALLOWED_HTML_TAGS, **CLEANER_KWARGS)
except ImportError:
    _cleaner = None

def clean_html(value):
    if _cleaner:
        return _cleaner.clean(value)
    
    raise ValueError("bleach.Cleaner not initialized, did you install bleach?")

