$(function () {
    function getCSRFToken() {
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function showMsg(type, text) {
        const $msg = $('#user-msg');
        $msg.removeClass('d-none alert-success alert-danger');
        $msg.addClass(type === 'success' ? 'alert-success' : 'alert-danger');
        $msg.text(text);
        setTimeout(() => $msg.addClass('d-none'), 2500);
    }

    // 统一的 AJAX POST 请求
    function ajaxPost(url, $btn, onSuccess) {
        const originalText = $btn.data('original-text') || $btn.text();
        $.ajax({
            url: url,
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            success: function (res) {
                if (res.code === 200) {
                    onSuccess(res);
                } else {
                    showMsg('error', res.msg || '操作失败');
                    $btn.prop('disabled', false).text(originalText);
                }
            },
            error: function (xhr) {
                showMsg('error', '网络错误，请重试');
                $btn.prop('disabled', false).text(originalText);
            }
        });
    }

    // 事件委托：所有按钮点击
    $('#user-list').on('click', '.btn-action', function () {
        const $btn = $(this);
        const url = $btn.data('url');
        const confirmMsg = $btn.data('confirm');
        if (!confirm(confirmMsg)) return;

        // 保存原始文本（如果之前没保存过）
        if (!$btn.data('original-text')) {
            $btn.data('original-text', $btn.text().trim());
        }
        const originalText = $btn.data('original-text');
        const actionType = originalText.trim();

        $btn.prop('disabled', true).text('处理中...');

        ajaxPost(url, $btn, function (res) {
            showMsg('success', res.msg);
            const $item = $btn.closest('.user-item');

            if (actionType === '删除') {
                // 删除：淡出该行
                $item.fadeOut(300, function () {
                    $(this).remove();
                });
            } else if (actionType === '禁用') {
                // 禁用：更新状态文本，切换按钮
                $item.find('.user-status-text').text('状态：禁用');
                $btn.removeClass('btn-warning').addClass('btn-success')
                    .text('启用')
                    .data('url', url.replace('deactivate', 'activate'))
                    .data('confirm', '确定启用该用户吗？')
                    .data('original-text', '启用')
                    .prop('disabled', false);
            } else if (actionType === '启用') {
                // 启用：更新状态文本，切换按钮
                $item.find('.user-status-text').text('状态：正常');
                $btn.removeClass('btn-success').addClass('btn-warning')
                    .text('禁用')
                    .data('url', url.replace('activate', 'deactivate'))
                    .data('confirm', '确定禁用该用户吗？')
                    .data('original-text', '禁用')
                    .prop('disabled', false);
            }
        });
    });
});