/**
 * Created by Евгений on 15.11.2014.
 */
function add_cart() {
    //удаляем предыдущие ошибки
    $('#add_button').html(' Отправка... ')
        .attr('disabled',true);
    $('div.error_item_form').remove();
    $('.has-error').removeClass('has-error');
    //заполняем описание
    d = $("#id_description").val();
    $.ajax({
        url: document.documentURI,
        type: "POST",
        dataType: "json",
        data: {
            product_slug: $("#id_product_slug").attr('value'),
            description : d,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            weight : $("#id_weight").val(),
            filling_choice : $("#id_filling_choice option:selected").val(),
            quantity :$("#id_quantity").val()
            //filling_choice_text: $("#id_filling_choice option:selected").text()
        },
        success: function(json) {
            if (json.success == 'False')
            {
                $('#add_button').html(' В корзину <i class="glyphicon glyphicon-shopping-cart icon-white"></i>')
                    .attr('disabled',false);
                for (var i = 0; i < json.errors.length; i++)
                {
                    $('#id_'+json.errors[i].key).parent().addClass('has-error');
                    $('#'+json.errors[i].key+'_error').html('<div class="error_item_form">' + json.errors[i].desc + '</div>')

                }
            }
            else if (json.success == 'True')
            {
                $('#add_button').css({'background-color':'#4CAE4C','width':'117'})
                    .html(' Добавлено! <i class="glyphicon glyphicon-ok icon-white"></i>').attr('disabled',true);
                $('#count_products').text(json.count);
                $('#go_cart').show();
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}

function prepareDocument() {
    $("#add_button").click(add_cart);
}

$(document).ready(prepareDocument);