/**
 * Created by Евгений on 07.12.2014.
 */

var rgx = /(\d)(?=(\d\d\d)+([^\d]|$))/g;

function css_address () {
    //this.css("padding-left","12px");
    alert( $(".my-form-control").css("padding-left"));
}

//удаление продукта из корзины
function remove_cart() {
    var tr = $(this).closest("tr");
    var name = tr.attr("id");
    var item_id = tr.find(".cart input[name='item_id']").val();
    $(this).attr('disabled',"disabled");
    $.ajax({
        url: document.documentURI,
        type: "POST",
        dataType: "json",
        data: {
            item_id: item_id,
            csrfmiddlewaretoken: $("#"+name +" .cart input[name='csrfmiddlewaretoken']").val(),
            submit : 'Remove'
        },
        success: function(json) {
            if (json.success == 'False') {
                //удаляем несуществующий продукт
                tr.remove();
                $('#count_products').text(json.count);
                s = json.cart_subtotal.toString().replace(rgx, '$1,');
                $(".cart_info_total h4").html("Всего: "+s+" р");
            }
            else if (json.success == 'True') {
                //удаляем продукт
                tr.remove();
                $('#count_products').text(json.count);
                s = json.cart_subtotal.toString().replace(rgx, '$1,');
                $(".cart_info_total h4").html("Всего: "+s+" р");
            }
            //если корзина оказалась пустой
            if (json.count ==0) {
                $("#cart tr").after("<tr><td colspan='7'>Ваша корзина пуста</td></tr>");
                $(".cart_info_total").remove();
                $("#send_checkout_button").attr('disabled',"disabled");
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}

function change_shipping() {
    if (this.value == '2') {
        $("#address_info").css("display", "none").fadeIn(500);
    }
    else {
        $("#address_info").fadeOut(500);
    }
}

function auto_fullname () {
    $("#fullname").suggestions({
        serviceUrl: "https://dadata.ru/api/v2",
        token: "c6df49053b76dbaaf973366d8f7b26f718a67638",
        type: "NAME",
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function(suggestion) {
            console.log(suggestion);
        }
    });
}


function init_shipping() {
    //alert($('input[type=radio][name=shipping]:checked').val());
    if ( $('input[type=radio][name=shipping]:checked').val() == 2) {
        //alert("Allot Thai Gayo Bhai");
        $("#address_info").css("display", "block");
    }
    else {
        $("#address_info").css("display", "none");
    }
}

//увеличение и уменьшение число товаров
function update_count () {
    var name = $(this).closest("tr").attr("id");
    var item_id = $("#"+name+" .cart input[name='item_id']").val();
    var quantity = $("#"+name+" .cart .item_quantity").html();
    var csrf = $("#"+name+" .cart input[name='csrfmiddlewaretoken']").val();
    if ($(this).attr("id") == "product_plus") {
        quantity=Number(quantity)+1;
    }
    else if ($(this).attr("id") == "product_minus") {
        if (quantity>=2) quantity-=1;
        else return false;
    }
    $.ajax({
        url: document.documentURI,
        type: "POST",
        dataType: "json",
        data: {
            item_id: item_id,
            quantity : quantity,
            csrfmiddlewaretoken: csrf,
            submit : 'Update'
        },
        success: function(json) {
            //удаляем несуществующий продукт
            if (json.success == 'False') {

                //alert("что-то пошло не так");
                $("#"+name).remove();
                $('#count_products').text(json.count);
                $(".cart_info_total h4").html("Всего: "+json.cart_subtotal.toString().replace(rgx, '$1,')+" р");
            }
            else if (json.success == 'True') {
                //изменяем кол-во
                $("#"+name+" .item_quantity").html(json.quantity);
                $("#"+name +" .total-td").html(json.total.toString().replace(rgx, '$1,')+" р");
                $(".cart_info_total h4").html("Всего: "+json.cart_subtotal.toString().replace(rgx, '$1,')+" р");
            }
            //если корзина оказалось пустой
            if (json.count ==0) {
                $("#cart tr").after("<tr><td colspan='7'>Ваша корзина пуста</td></tr>");
                $(".cart_info_total").remove();
                $("#send_checkout_button").attr('disabled',"disabled");
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}

function prepareDocument() {
    //alert($("#product_plus").closest(".cart").children("input[name='item_id']").val());
    /*$(".my-form-control").each(function () {
        this.style.setProperty( 'padding-left', '110px', 'important' );
    });*/
        //style("padding-left","110px","important");
    init_shipping();
    auto_fullname();

    $('input[type=radio][name=shipping]').change(change_shipping);

    $(".button-remove").click(remove_cart);
    $(".update_cart").click(update_count);
    //$(".my-form-control").click(css_adress);
}

$(document).ready(prepareDocument);