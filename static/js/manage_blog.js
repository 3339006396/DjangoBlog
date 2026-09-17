$(function () {
    function getCSRFToken() {
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function showMsg(type, text) {
        const $msg = $('#blog-msg');
        $msg.removeClass('d-none alert-success alert-danger');
        $msg.addClass(type === 'success' ? 'alert-success' : 'alert-danger');
        $msg.text(text);
        setTimeout(() => $msg.addClass('d-none'), 2500);
    }

    $('#blog-list').on('click', '.btn-delete-blog', function () {
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
                    const $item = $btn.closest('.blog-item');
                    $item.fadeOut(300, function () {
                        $(this).remove();
                        // 检查列表是否为空
                        if ($('#blog-list .blog-item').length === 0) {
                            $('#blog-list').html('<div class="col-12 text-center text-muted py-5" id="empty-hint"><p>暂无博客，<a href="{% url "blog:pub_blog" %}">去发布一篇</a></p></div>');
                        }
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