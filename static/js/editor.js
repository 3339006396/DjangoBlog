window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            // 调试用
            // console.log('editor content', editor.getHtml())
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    // 保存编辑器实例到全局变量，方便外部调用
    window.wangEditorInstance = editor

    // 记录编辑器最后可见的文本，作为提交时的兜底来源
    // （个别浏览器在富文本粘贴时可能出现“界面有字、编辑器模型为空”的情况）
    window.__editorVisibleText = ''
    const editorContainer = document.querySelector('#editor-container')
    if (editorContainer) {
        const capture = () => {
            setTimeout(() => {
                const s = editorContainer.querySelector('[data-slate-editor]')
                if (s && s.innerText && s.innerText.trim()) {
                    window.__editorVisibleText = s.innerText
                }
            }, 0)
        }
        editorContainer.addEventListener('beforeinput', capture)
        editorContainer.addEventListener('keyup', capture)
        editorContainer.addEventListener('paste', capture)
        editorContainer.addEventListener('compositionend', capture)
    }

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })
}
