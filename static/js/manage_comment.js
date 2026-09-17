$(function () {
    function getCSRFToken() {
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function showMsg(type, text) {
        const $msg = $('#comment-msg');
        $msg.removeClass('d-none alert-success alert-danger');
        $msg.addClass(type === 'success' ? 'alert-success' : 'alert-danger');
        $msg.text(text);
        setTimeout(() => $msg.addClass('d-none'), 2500);
    }

    $('#comment-list').on('click', '.btn-delete-comment', function () {
        const $btn = $(this);
        const url = $btn.data('url');
        if (!confirm($btn.data('confirm'))) return;
        $btn.prop('disabled', true).text('删除中...');

        $.ajax({
            url: url,
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            success: function (res) {
                if (res.code === 200) {
                    showMsg('success', res.msg);
                    $btn.closest('.comment-item').fadeOut(300, function () {
                        $(this).remove();
                    });
                } else {
                    showMsg('error', res.msg || '删除失败');
                    $btn.prop('disabled', false).text('删除');
                }
            },
            error: function () {
                showMsg('error', '网络错误，请重试');
                $btn.prop('disabled', false).text('删除');
            }
        });
    });
});