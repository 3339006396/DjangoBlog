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

    $('#comment-form').on('submit', function (e) {
        e.preventDefault();
        const $input = $('#comment');
        const $btn = $('#submit-comment-btn');
        const commentText = $input.val().trim();
        if (!commentText) {
            showMsg('error', '评论内容不能为空');
            return;
        }

        $btn.prop('disabled', true).text('提交中...');

        $.ajax({
            url: window.location.pathname,
            method: 'POST',
            data: $(this).serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            success: function (res) {
                if (res.code === 200) {
                    showMsg('success', res.msg);
                    // 追加到评论列表
                    const avatarUrl = res.avatar || '';
                    const username = res.username || '用户';
                    const now = new Date();
                    const timeStr = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0') + ' ' + String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
                    const newLi = $('<li>', {
                        class: 'list-group-item bg-dark text-white'
                    });
                    newLi.html(
                        '<div class="d-flex justify-content-between">' +
                        '<div>' +
                        '<img src="' + avatarUrl + '" alt="用户头像" class="rounded-circle" height="40px" width="40px">' +
                        '<span class="ms-2"></span>' +
                        '</div>' +
                        '<div class="align-self-center">' + timeStr + '</div>' +
                        '</div>' +
                        '<div class="mt-2 ms-5"></div>'
                    );
                    newLi.find('span.ms-2').text(username);
                    newLi.find('.mt-2').text(res.comment);
                    $('#comment-list').prepend(newLi);
                    // 更新评论数
                    const count = parseInt($('#comment-count').text()) + 1;
                    $('#comment-count').text(count);
                    $input.val('');
                } else {
                    showMsg('error', res.msg || '提交失败');
                }
            },
            error: function (xhr) {
                if (xhr.status === 403) {
                    showMsg('error', '请先登录后再评论');
                } else {
                    showMsg('error', '网络错误，请重试');
                }
            },
            complete: function () {
                $btn.prop('disabled', false).text('提交评论');
            }
        });
    });
});