const _proto_re = new RegExp('^(?:[a-z+]+:)?//', 'i');

function insertBaseURLWhenRelative (url) {
    if (!_proto_re.test(url)) {
        if (url.startsWith('/')) {
            url = `${window.location.origin}${url}`
        } else {
            url = `${window.location.origin}/${url}`
        }
    }
    return url;
}

class AceEditorController extends window.StimulusModule.Controller {
    static values = { 
        mode:                   {default: "ace/mode/django", type: String},
        theme:                  {default: "ace/theme/monokai", type: String},
        previewCheckboxChecked: {default: true, type: Boolean},
        useFramePreview:        {default: true, type: Boolean},
        frameCss:               {default: [], type: Array},
        frameJs:                {default: [], type: Array},
    };

    connect() {

        let frameCss = [];
        let frameJs = [];

        if (this.frameCssValue && this.frameCssValue.length > 0) {
            frameCss = this.frameCssValue.map(insertBaseURLWhenRelative);
        }

        if (this.frameJsValue && this.frameJsValue.length > 0) {
            frameJs = this.frameJsValue.map(insertBaseURLWhenRelative);
        }

        console.log('AceEditorController connected', this.modeValue, this.themeValue, this.useFramePreviewValue, frameCss, frameJs, this.previewCheckboxCheckedValue, this)

        this.editor = new AceEditorWidget(
            this.element.id,
            this.element.value,
            this.modeValue,
            this.themeValue,
            this.useFramePreviewValue,
            frameCss, 
            frameJs,
            this.previewCheckboxCheckedValue,
        );
    }

    disconnect() {
        this.editor.disconnect();
        this.editor = null;
    }
}

window.wagtail.app.register('ace-editor', AceEditorController);