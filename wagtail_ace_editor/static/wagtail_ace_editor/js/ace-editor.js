let previewables = [
    'ace/mode/html',
    'ace/mode/django',
]


class AceEditorWidget {
    constructor(querySelector, value = null, mode="ace/mode/django", theme="ace/theme/monokai", useFramePreview=false, frameCss=null, frameJs=null) {
        // Create the Ace Editor instance
        this.mode = mode;
        this.wrapper = document.querySelector(`#${querySelector}-wrapper`);
        this.element = this.wrapper.querySelector(`#${querySelector}-editor`);
        this.editor = ace.edit(this.element);

        this.editor.setTheme(theme); // Set a default theme
        this.editor.session.setMode(this.mode); // Set mode to HTML

        this.textArea = this.wrapper.querySelector(`#${querySelector}`);
        this.previewWrapper = document.querySelector(`#${querySelector}-preview-wrapper`);
        this.previewCheckbox = this.wrapper.querySelector(`#${querySelector}-preview-check`);

        this.useFramePreview = useFramePreview;
        this.frameCss = frameCss;
        this.frameJs = frameJs;

        if (this.previewWrapper) {
            this.editor.getSession().on('change', this.setPreviewText.bind(this));
            this.previewCheckbox.addEventListener('change', this._setPreviewing.bind(this));
            this.previewCheckbox.checked = previewables.includes(this.mode);
            this._setPreviewing();
        }

        // Set the initial value if provided
        if (value !== null) {
            this.editor.setValue(value);
        }
        this.editor.clearSelection();
    }

    setPreviewText() {
        let value = this.editor.getValue();
        value = value.trim();
        this.textArea.value = value;
        if (this.previewWrapper && this.previewCheckbox.checked) {
            this._setPreviewText(value);
        }
    }

    _setPreviewText(value) {
        if (this.useFramePreview && this.iframeDoc && previewables.includes(this.mode)) {
            this.iframeDoc.open();
            this.iframeDoc.write(`<!DOCTYPE html><html><head>${this.styleHtml}</head><body>${value}</body>${this.scriptHtml}</html>`); // or `<script>${value}</script>
            this.iframeDoc.close();
        } else {
            this.previewText.innerText = value;
        }
    }

    _setPreviewing() {
        if (this.previewCheckbox.checked) {
            this.previewWrapper.classList.add('ace-editor-widget-previewing');
            if (this.useFramePreview && !this.iframe && previewables.includes(this.mode)) {
                this.iframe = document.createElement('iframe');
                this.iframe.classList.add('ace-editor-widget-preview-iframe');
                this.previewWrapper.innerHTML = '';
                this.previewWrapper.appendChild(this.iframe);
                this.iframeDoc = this.iframe.contentWindow.document;

                let styleWrapper    = document.createElement('div');
                let scriptWrapper   = document.createElement('div');

                for (let css of (this.frameCss || [])) {
                    let link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.href = css;
                    styleWrapper.appendChild(link);
                }

                for (let js of (this.frameJs || [])) {
                    let script = document.createElement('script');
                    script.src = js;
                    scriptWrapper.appendChild(script);
                }

                this.styleHtml = styleWrapper.innerHTML;
                this.scriptHtml = scriptWrapper.innerHTML;
            } else {
                this.previewText = document.createElement('div');
                this.previewText.classList.add('ace-editor-widget-nomarkup');
                this.previewWrapper.appendChild(this.previewText);
            }
            this._setPreviewText(this.editor.getValue());
        } else {
            this.previewWrapper.classList.remove('ace-editor-widget-previewing');
            if (this.iframe) {
                this.iframe.remove();
                this.iframe = null;
                this.iframeDoc = null;
            } else if (this.previewText) {
                this.previewText.remove();
            }
            this.previewWrapper.innerHTML = '';
        }
    }


    setState(value) {
        if (value !== null && value !== undefined && value !== 'None') {
            value = value.trim();
            this.editor.setValue(value);
        } else {
            this.editor.setValue(''); // or set some default value
        }
        this.editor.clearSelection();
        this.setPreviewText();
    }

    getState() {
        // This method is ambiguous in the context of Ace Editor. If needed, customize accordingly.
        return this.editor.getValue();
    }

    getValue() {
        return this.editor.getValue();
    }

    focus() {
        this.editor.focus();
    }

    disconnect() {
        this.editor.setValue(''); // or set some default value
        this.editor.destroy();
    }
}
