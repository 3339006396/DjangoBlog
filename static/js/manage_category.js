$(function() {
        function getCSRFToken() {
            const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
            return match ? decodeURIComponent(match[1]) : '';
        }
        function showMsg(type, text) {
            const $msg = $('#category-msg');
            $msg.removeClass('d-none alert-success alert-danger');
            $msg.addClass(type === 'success' ? 'alert-success' : 'alert-danger');
            $msg.text(text);
            setTimeout(() => $msg.addClass('d-none'), 2500);
        }

        // 添加分类
        $('#add-category-form').on('submit', function(e) {
            e.preventDefault();
            const $input = $('#category-name-input');
            const $btn = $('#add-category-btn');
            const $err = $('#category-error-msg');
            $err.addClass('d-none').text('');

            const name = $input.val().trim();
            if (!name) {
                $err.removeClass('d-none').text('分类名称不能为空');
                return;
            }

            $btn.prop('disabled', true).text('添加中...');
            const formData = $(this).serialize();

            $.ajax({
                url: $(this).attr('action'),
                method: 'POST',
                data: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                },
                success: function(res) {
                    if (res.code === 200) {
                        showMsg('success', res.msg);
                        // 动态添加到列表
                        const newLi = $('<li>', {
                            class: 'list-group-item bg-dark text-white d-flex justify-content-between align-items-center category-item',
                            html: '<span class="category-name"></span>' +
                                  '<button type="button" class="btn btn-sm btn-danger btn-delete-category" data-confirm="确定删除这个分类吗？">删除</button>'
                        });
                        newLi.find('.category-name').text(res.name);
                        // 使用新 ID 构造 URL
                        const deleteUrl = "{% url 'admin:delete' 'category' 0 %}".replace('/0/', '/' + res.id + '/');
                        newLi.find('.btn-delete-category').data('url', deleteUrl);
                        $('#category-list').append(newLi);
                        $input.val('');
                    } else {
                        let errText = res.msg || '添加失败';
                        if (res.errors) {
                            const firstKey = Object.keys(res.errors)[0];
                            errText = res.errors[firstKey][0] || errText;
                        }
                        $err.removeClass('d-none').text(errText);
                    }
                },
                error: function(xhr) {
                    if (xhr.responseJSON && xhr.responseJSON.errors) {
                        const firstKey = Object.keys(xhr.responseJSON.errors)[0];
                        $err.removeClass('d-none').text(xhr.responseJSON.errors[firstKey][0]);
                    } else {
                        showMsg('error', '网络错误，请重试');
                    }
                },
                complete: function() {
                    $btn.prop('disabled', false).text('添加');
                }
            });
        });

        // 删除分类
        $('#category-list').on('click', '.btn-delete-category', function() {
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
                success: function(res) {
                    if (res.code === 200) {
                        showMsg('success', res.msg);
                        $btn.closest('.category-item').fadeOut(300, function() { $(this).remove(); });
                    } else {
                        showMsg('error', res.msg || '删除失败');
                        $btn.prop('disabled', false).text('删除');
                    }
                },
                error: function() {
                    showMsg('error', '网络错误，请重试');
                    $btn.prop('disabled', false).text('删除');
                }
            });
        });
    });