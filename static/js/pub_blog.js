// 获取 Cookie 中的 CSRF Token
function getCSRFToken() {
    const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
    return match ? decodeURIComponent(match[1]) : '';
}

// 更新表单中的 CSRF Token
function updateCSRFToken(form) {
    const newToken = getCSRFToken();
    if (newToken) {
        const csrfInput = form.querySelector('[name="csrfmiddlewaretoken"]');
        if (csrfInput) {
            csrfInput.value = newToken;
        }
    }
}

function escapeHtml(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

// 获取编辑器内容（保留 HTML 格式）
async function getEditorContent() {
    const editor = window.wangEditorInstance;

    // 方法1: 使用编辑器实例的 getHtml 方法（如果存在）
    if (editor && typeof editor.getHtml === 'function') {
        // 中文输入法组合输入时，Slate 模型尚未更新，getHtml() 会返回空。
        // 先让编辑器失焦以提交组合内容，避免误判为“内容为空”。
        const slateEl = document.querySelector('#editor-container [data-slate-editor]');
        if (slateEl && document.activeElement === slateEl) {
            try {
                if (typeof editor.blur === 'function') editor.blur();
            } catch (e) {
                console.error('editor.blur() 失败:', e);
            }
        }

        let content = editor.getHtml();

        // 组合输入提交后，模型更新是异步的，稍等片刻再读一次
        if (!content || content === '<p><br></p>' || content === '<p></p>') {
            await new Promise(resolve => setTimeout(resolve, 60));
            content = editor.getHtml();
        }

        if (content && content !== '<p><br></p>' && content !== '<p></p>') {
            console.log('getHtml():', content);
            return content;
        }

        // getHtml() 仍为空但编辑器里有可见文本时，用可见文本兜底
        const domText = slateEl && slateEl.innerText ? slateEl.innerText : '';
        const text = domText.trim() ? domText : (window.__editorVisibleText || '');
        const lines = text.split(/\n+/).map(s => s.trim()).filter(Boolean);
        if (lines.length) {
            const fallbackHtml = lines.map(line => '<p>' + escapeHtml(line) + '</p>').join('');
            console.log('文本兜底:', fallbackHtml);
            return fallbackHtml;
        }
        return '';
    }

    // 方法2: 编辑器实例缺失（初始化失败）时，直接从 DOM 获取
    const selectors = [
        '#editor-container [data-slate-editor]',
        '#editor-container .w-e-text-container',
        '#editor-container .w-e-scroll',
        '#editor-container'
    ];
    for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el && el.innerHTML && el.innerHTML.trim() && el.innerHTML !== '<p><br></p>') {
            // 从编辑器根元素提取：只取 [data-slate-editor] 的内容
            const slateEditor = el.querySelector('[data-slate-editor]');
            if (slateEditor) {
                return slateEditor.innerHTML;
            }
            return el.innerHTML;
        }
    }
    return '';
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('pub-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        const btn = document.getElementById('submit-btn');
        const msgEl = document.getElementById('publish-msg');
        const form = e.target;

        function showMsg(type, text) {
            msgEl.classList.remove('d-none', 'alert-success', 'alert-danger');
            msgEl.classList.add(type === 'success' ? 'alert-success' : 'alert-danger');
            msgEl.textContent = text;
        }

        // 提交前先更新 CSRF Token（防止第一次提交后 Token 被轮换）
        updateCSRFToken(form);

        // 获取编辑器内容（保留 HTML 格式）
        const content = await getEditorContent();

        console.log('最终 content:', content);
        console.log('editor-container innerHTML:', document.querySelector('#editor-container')?.innerHTML?.substring(0, 200));

        document.querySelector('#content').value = content;

        // 客户端校验
        const title = document.getElementById('title').value.trim();
        const category = document.getElementById('category').value;
        // 去除 HTML 标签后判断是否为空
        const plainText = content.replace(/<[^>]+>/g, '').replace(/&nbsp;/gi, ' ').trim();
        if (!title) {
            showMsg('error', '请输入标题');
            return;
        }
        if (!category) {
            showMsg('error', '请选择分类');
            return;
        }
        if (!plainText) {
            console.error('内容为空时捕获到的 content:', JSON.stringify(content));
            const snippet = content ? '（捕获到内容：' + content.substring(0, 80) + '…）' : '（未捕获到任何内容）';
            showMsg('error', '内容不能为空' + snippet);
            return;
        }

        btn.disabled = true;
        try {
            const resp = await fetch('', {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()  // 主动带上 CSRF Token
                }
            });

            // 提交成功后，从响应头或 Cookie 获取新的 CSRF Token
            // Django 成功处理 POST 后会轮换 Token
            const newCsrfToken = resp.headers.get('X-CSRFToken') || getCSRFToken();
            if (newCsrfToken) {
                const csrfInput = form.querySelector('[name="csrfmiddlewaretoken"]');
                if (csrfInput) {
                    csrfInput.value = newCsrfToken;
                }
            }

            let data;
            try {
                data = await resp.json();
            } catch (err) {
                // 非 JSON 响应：可能是登录页重定向或 CSRF 403 错误
                if (resp.status === 403) {
                    showMsg('error', '请求被拒绝，请刷新页面后重试');
                } else if (resp.redirected) {
                    showMsg('error', '登录已过期，请重新登录');
                } else {
                    showMsg('error', '发布失败，请重试');
                }
                return;
            }

            if (data.code === 200) {
                showMsg('success', data.msg || '博客发布成功');
                setTimeout(function () {
                    window.location.href = window.pubBlogIndexUrl || '/';
                }, 800);
            } else {
                const errors = data.errors || {};
                const firstKey = Object.keys(errors)[0];
                showMsg('error', firstKey ? errors[firstKey][0] : (data.msg || '发布失败'));
            }
        } catch (err) {
            showMsg('error', '网络错误，发布失败，请重试');
        } finally {
            btn.disabled = false;
        }
    });
});
