wagtail_ace_editor
==================

Wagtail Ace Editor is a simple extension which provides access to the [Ace Editor Library](https://github.com/ajaxorg/ace).

Usage is simple and easy like you're used to from any django widget.

We provide a custom theme based on the default cobalt theme to fit into your wagtail application - this is the default theme.

The full library from [Ace Editor on UNPKG](https://unpkg.com/ace-builds@1.3.3/src-min/) has been included to be used.

This is for the people who want full control over their django templates for a specific page at runtime, or want to edit and create plain HTML.

It is a very powerfull block/widget, which can be used to provide django template functionality at runtime.

You will be able to have full access to the RequestContext of a regular Django template.

## Note

This widget is only for use in the wagtail's admin area - it does not do anything for your frontend.

If demand for this appears to be high in the future it will be added.

Quick start
-----------

1. Add 'wagtail_ace_editor' to your INSTALLED_APPS setting like this:

   ```
   INSTALLED_APPS = [
   ...,
   'wagtail_ace_editor',
   ]
   ```
2. Run `py manage.py collectstatic` to collect all the relevant javascript and css files.
3. Simply import the widget, or blocks into your django application and use them!

   ```python
   from wagtail_ace_editor.blocks import AceEditorBlock
   from wagtail_ace_editor.widgets import AceEditorWidget
   # Formfield: from wagtail_ace_editor.forms import AceEditorField

   # ... other imports

   class MyModel(models.Model):
       	html_field = models.TextField(
   		...
   	)

   	content = StreamField([
   		('html_block', AceEditorBlock(
   			... Parameters
   		)),
    	])

   	panels = [
   		FieldPanel("html_field", widget=AceEditorWidget(
   			... Parameters
   		)),
   		FieldPanel("content"),
   	]

   ```

# Parameters

### mode

**Mode to use for your ace editor.**

What type of code do you want to edit? See the full catalog of [ace.js](https://unpkg.com/ace-builds@1.3.3/src-min/) modes.

`mode="ace/mode/django"`

### theme

**Theme to use for your ace editor.**

`theme="ace/theme/wagtail"`

### include_template_context (default False)

**Include parent template context when using wagtail's {% include_block %} method.**

I mean - why else would you use tempates? When this is true and the mode is ace/mode/(html or django)

the template will be rendered using django's `render_to_string`. Otherwise it will be output as HTML.

*(Only for use in the block!)*
`include_template_context: bool`

### use_frame_preview (default False)

**Render ace/mode/(html or django) inside of an iFrame as opposed to escaping it.**

`use_frame_preview: bool`

### frame_css (default None)

**When using ace/mode/(html or django), allows you to pass in custom CSS to style the iFrame**

If the path is relative, the `STATIC_URL` prefix will be appended to it.

`frame_css: list[str]`

### frame_js (default None)

**When using ace/mode/(html or django), allows you to pass in custom JS to script inside of iFrame**

If the path is relative, the `STATIC_URL` prefix will be appended to it.

`frame_js: list[str]`

### preview_checkbox_checked (default True)

**When using ace/mode/(html or django), allows you to set the default state of the preview checkbox**

`preview_checkbox_checked: bool`

### disable_preview (default False)

**Allows to disable the preview window** 

`disable_preview: bool`

### clean_html (default false)

**If you are using `ace/mode/html` or `ace/mode/django` we allow you to clean the HTML if the parameter is specified.**

This might be useful if you want to include the full django-template or HTML editing experience yet still not let the user define any (inline) styles/javascript.

- *Will only work if [bleach ](https://pypi.org/project/bleach/)is installed!*
- *Will not work for the preview in the wagtail admin!*

`clean_html: bool`

#### Settings for cleaning (settings.py)

##### BLEACH_CLEAN_ACE_MODES

**Modes to use the bleach cleaner on.**

By default we clean the modes ace/mode/django and ace/mode/html.

`BLEACH_CLEAN_ACE_MODES: list[str]`

##### ALLOWED_HTML_TAGS

**HTML tags to allow for the bleach cleaner itself.**
By default all tags except Style and Script.

`ALLOWED_HTML_TAGS: list[str]`

##### CLEANER_KWARGS

**Extra keyword arguments to supply to the bleach.sanitizer.Cleaner class**
`CLEANER_KWARGS: dict`
