/**
 * Created by Евгений on 15.11.2014.
 */


function add_cart_from_catalog() {
    var id = this.id;
    $('#'+id+'_button').html(' Отправка... ').attr('disabled',true);
    //$(this).html("Отправка...");
    //alert("ага!");
    //alert(id);
    $.ajax({
        url: document.documentURI,
        type: "POST",
        dataType: "json",
        data: {
            product_slug: id,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        },
        success: function(json) {
            if (json.success == 'False')
            {
                alert("error!"+json.errors);
            }
            else if (json.success == 'True')
            {
                //alert("добавили!");
                $('#'+id+'_button').css({'background-color':'#4CAE4C'})
                    .html('  Добавлено! <i class="glyphicon glyphicon-ok icon-white"></i>').attr('disabled',true);
                $('#count_products').text(json.count);
               /*// $('#go_cart').show();
                setTimeout(function (id) {
                    $('#'+id+'_button')
                        .closest(".add_order")
                        .html("<div class = 'detail_button'> Оформить <i class='glyphicon glyphicon-shopping-cart icon-white'></i></div>")
                        .css({'font-size' : '17px' ,'color':'#6E4A29'});
                    $('.detail_button').css({'background-color':'#DDB66F'});

                    *//*.html('<a href="#"> Перейти в корзину </a>! ').attr('disabled',false)
                        .css({'font-size':'15px'});*//*
                    alert(id)
                }, 1000, id);*/
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}

function change_button(id) {
    $('#'+id+'_button') .html(' Перейти в корзину ! ').attr('disabled',false);
}


function sort_products() {
    var pred_id = $(this).attr('id');
    id = pred_id;
    $("#fon").css({'display':'block'});
    $("#load").fadeIn(1000);
    switch (id) {
        case "name":
            {
                document.getElementById('name').id = 'namea';
                id = 'namea';
                break
            }
        case "namea":
            {
                document.getElementById('namea').id = 'named';
                id = 'named';
                break
            }
        case "named":
            {
                document.getElementById('named').id = 'namea';
                id = 'namea';
                break
            }
        case "price":
            {
                document.getElementById('price').id = 'pricea';
                id = 'pricea';
                break
            }
        case "pricea":
            {
                document.getElementById('pricea').id = 'priced';
                id = 'priced';
                break
            }
        case "priced":
            {
                document.getElementById('priced').id = 'pricea';
                id = 'pricea';
                break
            }
    }
    $.get(document.documentURI, {
        category_id: id
    }, function(data) {
        $.ajax({
            success: function() {
                $("#show_products .row").html(data).hide().fadeIn(1000);
                var s_n = $(".sort_n");
                var s_p = $(".sort_p");
                if (pred_id !== "name" && id == "namea") {
                    $("#my_glyphicon_name").replaceWith("<i id=\"my_glyphicon_name\" class=\"glyphicon glyphicon-arrow-up icon-arrow-up\"></i>")
                    $("#my_glyphicon_name").css({
                        'visibility': 'visible'
                    });
                    $("#my_glyphicon_price").css({
                        'visibility': 'hidden'
                    });
                    s_n.css({
                        'color': '#9c906f'
                    });
                    s_p.css({
                        'color': '#4e3d20'
                    });
                    if (s_p.attr('id') == "priced")
                        document.getElementById('priced').id = "price";
                    else if (s_p.attr('id') == "pricea")
                        document.getElementById('pricea').id = "price";
                } else if (id == "named") {
                    $("#my_glyphicon_name").replaceWith("<i id=\"my_glyphicon_name\" class=\"glyphicon glyphicon-arrow-down icon-arrow-down\"></i>")
                    $("#my_glyphicon_name").css({
                        'visibility': 'visible'
                    });
                    $("#my_glyphicon_price").css({
                        'visibility': 'hidden'
                    });
                    s_n.css({
                        'color': '#9c906f'
                    });
                    s_p.css({
                        'color': '#4e3d20'
                    });
                    if (s_p.attr('id') == "priced")
                        document.getElementById('priced').id = "price";
                    else if (s_p.attr('id') == "pricea")
                        document.getElementById('pricea').id = "price";
                } else if (pred_id !== "price" && id == "pricea") {
                    $("#my_glyphicon_price").replaceWith("<i id=\"my_glyphicon_price\" class=\"glyphicon glyphicon-arrow-up icon-arrow-up\"></i>")
                    $("#my_glyphicon_price").css({
                        'visibility': 'visible'
                    });
                    $("#my_glyphicon_name").css({
                        'visibility': 'hidden'
                    });
                    s_p.css({
                        'color': '#9c906f'
                    });
                    s_n.css({
                        'color': '#4e3d20'
                    });
                    if (s_n.attr('id') == "named")
                        document.getElementById('named').id = "name";
                    else if (s_n.attr('id') == "namea")
                        document.getElementById('namea').id = "name";
                } else if (id == "priced") {
                    $("#my_glyphicon_price").replaceWith("<i id=\"my_glyphicon_price\" class=\"glyphicon glyphicon-arrow-down icon-arrow-down\"></i>")
                    $("#my_glyphicon_price").css({
                        'visibility': 'visible'
                    });
                    $("#my_glyphicon_name").css({
                        'visibility': 'hidden'
                    });
                    s_p.css({
                        'color': '#9c906f'
                    });
                    s_n.css({
                        'color': '#4e3d20'
                    });
                    if (s_n.attr('id') == "named")
                        document.getElementById('named').id = "name";
                    else if (s_n.attr('id') == "namea")
                        document.getElementById('namea').id = "name";
                } else if (pred_id == "price" && id == "pricea") {
                    $("#my_glyphicon_price").replaceWith("<i id=\"my_glyphicon_price\" class=\"glyphicon glyphicon-arrow-up icon-arrow-up\"></i>")
                    $("#my_glyphicon_price").css({
                        'visibility': 'visible'
                    });
                    $("#my_glyphicon_name").css({
                        'visibility': 'hidden'
                    });
                    s_p.css({
                        'color': '#9c906f'
                    });
                    s_n.css({
                        'color': '#4e3d20'
                    });
                    if (s_n.attr('id') == "named")
                        document.getElementById('named').id = "name";
                    else if (s_n.attr('id') == "namea")
                        document.getElementById('namea').id = "name";
                } else if (pred_id == "name" && id == "namea") {
                    $("#my_glyphicon_name").replaceWith("<i id=\"my_glyphicon_name\" class=\"glyphicon glyphicon-arrow-up icon-arrow-up\"></i>");
                    $("#my_glyphicon_name").css({
                        'visibility': 'visible'
                    });
                    $("#my_glyphicon_price").css({
                        'visibility': 'hidden'
                    });
                    s_n.css({
                        'color': '#9c906f'
                    });
                    s_p.css({
                        'color': '#4e3d20'
                    });
                    if (s_p.attr('id') == "priced")
                        document.getElementById('priced').id = "price";
                    else if (s_p.attr('id') == "pricea")
                        document.getElementById('pricea').id = "price";
                }
                $("#fon").css({'display':'none'});
                $("#load").css({'display':'none'});
                $('.add_form').submit(add_cart_from_catalog);
                load_products();
            }
        });
    });
}

function load_products() {
    //alert("lazy");
    $("img.lazy_load").lazyload({
        effect : "fadeIn"
    });
    /*$(".products_min").css("display", "none").fadeIn(500);
    $(".category_min").css("display", "none").fadeIn(500);*/
}

$(function () {
    $.scrollUp({
        topDistance: '590',
        animation: 'fade',
        scrollText: 'Наверх'
    });
});

function prepareDocument() {
    load_products();
    $(".sort span").click(sort_products);
    $('.add_form').submit(add_cart_from_catalog);
}


$(document).ready(prepareDocument);