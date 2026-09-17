$(function () {
    console.log('[Login] JS loaded');

    function getCSRFToken() {
        const input = document.querySelector('[name="csrfmiddlewaretoken"]');
        if (input && input.value) return input.value;
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function showFieldError(fieldName, message) {
        if (fieldName === '__all__') {
            alert(message);
            return;
        }
        const $field = $('[name="' + fieldName + '"]');
        if (!$field.length) return;
        $field.removeClass('is-invalid');

        // input-group 内的字段：错误显示在整个 input-group 下面
        let $container = $field.closest('.input-group');
        let $errDiv;
        if ($container.length) {
            $errDiv = $container.next('.field-error');
            if (!$errDiv.length) {
                $errDiv = $('<div class="field-error text-danger small mt-1"></div>');
                $container.after($errDiv);
            }
        } else {
            $errDiv = $field.siblings('.field-error');
            if (!$errDiv.length) {
                $errDiv = $('<div class="field-error text-danger small mt-1"></div>');
                $field.after($errDiv);
            }
        }

        if (message) {
            $field.addClass('is-invalid');
            $errDiv.text(message).show();
        } else {
            $errDiv.hide().text('');
        }
    }

    function clearAllErrors() {
        $('.field-error').hide().text('');
        $('input').removeClass('is-invalid');
    }

    $('#login-form').on('submit', function (e) {
        e.preventDefault();
        clearAllErrors();

        const $form = $(this);
        const url = $form.attr('action') || window.location.pathname;
        const $btn = $form.find('button[type="submit"]');
        $btn.prop('disabled', true).text('登录中...');

        $.ajax({
            url: url,
            method: 'POST',
            data: $form.serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            success: function (res) {
                console.log('[Login] Response:', res);
                if (res.code === 200) {
                    alert('登录成功，即将跳转');
                    window.location.href = res.redirect;
                } else if (res.code === 400 && res.errors) {
                    $.each(res.errors, function (field, messages) {
                        showFieldError(field, messages[0]);
                    });
                } else {
                    alert(res.msg || '登录失败');
                }
            },
            error: function (xhr) {
                let parsed = null;
                try { parsed = JSON.parse(xhr.responseText); } catch (e) {}
                if (parsed && parsed.errors) {
                    $.each(parsed.errors, function (field, messages) {
                        showFieldError(field, messages[0]);
                    });
                } else if (parsed && parsed.msg) {
                    alert(parsed.msg);
                } else {
                    alert('网络错误，请重试');
                }
            },
            complete: function () {
                $btn.prop('disabled', false).text('登录');
            }
        });
    });

    console.log('[Login] All bindings set up');
});