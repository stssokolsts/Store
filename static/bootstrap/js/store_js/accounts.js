/**
 * Created by Евгений on 26.11.2014.
 */

function login(e) {
    //удаляем предыдущие ошибки
    $('.has-error').removeClass('has-error');
    e.preventDefault();
    $.ajax({
        url: $("#login_form").attr('action'),
        type: "POST",
        dataType: "json",
        data: {
            username: $( "#login_form #id_username").val(),
            password : $("#login_form #id_password").val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function(json) {
            if (json.success == 'False')
            {
                $('#login-tab .alert').css('display','block');
                $('#login_errorlist h5').html('Авторизация не удалась');
                for (var i = 0; i < json.errors.length; i++)
                {
                    $('#id_'+json.errors[i].key).parent().addClass('has-error');
                    $('#login_errorlist .error_description').html(json.errors[i].desc)

                }
            }
            else if (json.success == 'True')
            {
                if (json.response)
                    location = json.response;
                else
                {
                    location.reload();
                    //$('#myModal').modal('hide');
                }
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}


function registration(e) {
    $('div.error_item_form').remove();
    $('.has-error').removeClass('has-error');
    //заполняем описание
    $.ajax({
        url: $("#reg_form").attr('action'),
        type: "POST",
        dataType: "json",
        data: {
            name: $("#id_name").val(),
            email: $("#id_email").val(),
            password1: $("#id_password1").val(),
            password2: $("#id_password2").val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function(json) {
            alert(json.success);
            if (json.success == false)
            {
                for (var i = 0; i < json.errors.length; i++)
                {
                    $('#id_'+json.errors[i].key).parent().addClass('has-error');
                    $('#'+json.errors[i].key+'_error').html('<div class="error_item_form">' + json.errors[i].desc + '</div>')

                }
            }
            else if (json.success == true)
            {
                $('#myModal').modal('hide');
                location.reload();
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}


function showregister() {
    $('#li_register').tab('show');
    $('#sign_up_modal').modal();
    return false
}

function showlogin() {
    $('#li_login').tab('show');
    $('#sign_up_modal').modal();
    return false
}

function prepareDocument() {
    $("#login_form").on("submit",login);
    $("#reg_form").on("submit",registration);
    $('.get-reg-modal').on("click",showregister);
    $('.get-login-modal').on("click",showlogin);
    //$("#login_button").onclick(login)
}



$(document).ready(prepareDocument);