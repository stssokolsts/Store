/**
 * Created by Евгений on 07.12.2014.
 */

function remove_cart() {
    var name = $(this).attr('id');
    $(this).attr('disabled',"disabled");
    $.ajax({
        url: document.documentURI,
        type: "POST",
        dataType: "json",
        data: {
            item_id: $("#"+name +"_form input[name='item_id']").val(),
            csrfmiddlewaretoken: $("#"+name +"_form input[name='csrfmiddlewaretoken']").val(),
            submit : 'Remove'
        },
        success: function(json) {
            alert(json);
            if (json.success == 'False') {
                //alert("что-то пошло не так");
                $("#"+name+"_tr").remove();
                $('#count_products').text(json.count);
            }
            else if (json.success == 'True') {
                //alert("все круто");
                $("#"+name+"_tr").remove();
                if (json.count ==0) {
                    $("#cart tr").after("<tr><td colspan='7'>Ваша корзина пуста</td></tr>");
                    $(".cart_info_total").remove()
                }
                $('#count_products').text(json.count);
                $(".cart_info_total h4").html("Всего: "+json.cart_subtotal+" р");
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}

function prepareDocument() {
    $(".button-remove").click(remove_cart);
}

$(document).ready(prepareDocument);