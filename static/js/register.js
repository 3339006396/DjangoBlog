$(function () {
    console.log('[Register] JS loaded');

    function getCSRFToken() {
        // 优先从隐藏表单字段获取
        const input = document.querySelector('[name="csrfmiddlewaretoken"]');
        if (input && input.value) {
            console.log('[Register] CSRF from input:', input.value.substring(0, 8) + '...');
            return input.value;
        }
        // 备选：从 cookie 获取
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]*)/);
        if (match) {
            console.log('[Register] CSRF from cookie:', match[1].substring(0, 8) + '...');
            return decodeURIComponent(match[1]);
        }
        console.warn('[Register] CSRF token not found!');
        return '';
    }

    function showFieldError(fieldName, message) {
        console.log('[Register] showFieldError:', fieldName, '=', message);
        if (fieldName === '__all__') {
            alert(message);
            return;
        }
        const $field = $('[name="' + fieldName + '"]');
        if (!$field.length) {
            console.warn('[Register] Field not found:', fieldName);
            return;
        }
        $field.removeClass('is-invalid');

        // 确定错误提示的插入位置
        let $container = $field.closest('.input-group');
        let $errDiv;
        if ($container.length) {
            // 在 input-group 里：错误显示在整个 input-group 下面
            $errDiv = $container.next('.field-error');
            if (!$errDiv.length) {
                $errDiv = $('<div class="field-error text-danger small mt-1"></div>');
                $container.after($errDiv);
            }
        } else {
            // 普通字段：错误显示在 input 下面
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

    function bindCaptchaBtn() {
        $("#get_captcha_btn").on("click", function () {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("请输入邮箱");
                return;
            } else if (!email.includes("@")) {
                alert("请输入正确的邮箱格式");
                return;
            }
            $this.prop('disabled', true);
            $.ajax("/auth/captcha/?email=" + email, {
                method: "GET",
                success: function (result) {
                    if (result["code"] === 200) {
                        alert("验证码发送成功");
                    } else {
                        alert(result["message"]);
                        $this.prop('disabled', false);
                    }
                },
                error: function () {
                    alert("网络错误，请重试");
                    $this.prop('disabled', false);
                }
            });
            let countdown = 60;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text("重新获取");
                    $this.prop('disabled', false);
                    clearInterval(timer);
                } else {
                    $this.text(countdown + "秒");
                    countdown--;
                }
            }, 1000);
        });
    }

    // 注册表单 AJAX 提交
    $('#register-form').on('submit', function (e) {
        e.preventDefault();
        console.log('[Register] Form submit intercepted');
        clearAllErrors();

        const $form = $(this);
        const url = $form.attr('action') || window.location.pathname;
        console.log('[Register] AJAX URL:', url);

        const $btn = $form.find('button[type="submit"]');
        $btn.prop('disabled', true).text('注册中...');

        const csrfToken = getCSRFToken();
        console.log('[Register] CSRF token:', csrfToken ? 'found' : 'MISSING!');

        $.ajax({
            url: url,
            method: 'POST',
            data: $form.serialize(),
            dataType: 'json',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            success: function (res) {
                console.log('[Register] AJAX success, response:', res);
                if (res.code === 200) {
                    alert('注册成功，即将跳转到登录页');
                    window.location.href = res.redirect;
                } else if (res.code === 400 && res.errors) {
                    console.log('[Register] Validation errors:', res.errors);
                    $.each(res.errors, function (field, messages) {
                        showFieldError(field, messages[0]);
                    });
                } else {
                    alert(res.msg || '注册失败');
                }
            },
            error: function (xhr, status, err) {
                console.log('[Register] AJAX error:', status, err);
                console.log('[Register] Response:', xhr.responseText);
                // 尝试从错误响应中解析 JSON
                let parsed = null;
                try {
                    parsed = JSON.parse(xhr.responseText);
                } catch (e) {}
                if (parsed && parsed.errors) {
                    $.each(parsed.errors, function (field, messages) {
                        showFieldError(field, messages[0]);
                    });
                } else if (parsed && parsed.msg) {
                    alert(parsed.msg);
                } else if (xhr.status === 403) {
                    alert('CSRF 验证失败，请刷新页面重试');
                } else {
                    alert('网络错误 (' + xhr.status + ')，请重试');
                }
            },
            complete: function () {
                $btn.prop('disabled', false).text('注册');
            }
        });
    });

    bindCaptchaBtn();
    console.log('[Register] All bindings set up');
});