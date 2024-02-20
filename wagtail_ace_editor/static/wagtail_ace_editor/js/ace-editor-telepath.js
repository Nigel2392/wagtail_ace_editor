

(function() {
    function AceEditorWidgetInput(html, _, mode) {
        this.html = html;
        this.mode = mode;
    }
    AceEditorWidgetInput.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;


        var aceEditor = new AceEditorWidget(id, initialState, this.mode);
        aceEditor.setState(initialState);
        return aceEditor;
    };

    window.telepath.register('blockapp.widgets.AceEditorWidget', AceEditorWidgetInput);
})();
