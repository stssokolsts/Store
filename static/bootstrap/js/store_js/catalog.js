/**
 * Created by Евгений on 15.11.2014.
 */

function add_cart_from_catalog() {
    var id = this.id;
    alert(id);
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
                alert("добавили!");
                $('#'+id+'_button').css({'background-color':'#4CAE4C','width':'117'})
                    .html(' Добавлено! <i class="glyphicon glyphicon-ok icon-white"></i>').attr('disabled',true);
                $('#count_products').text(json.count);
               // $('#go_cart').show();
            }
        },
        error: function(xhr, errmsg, err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    });
    return false;
}

function sort_products() {
    var pred_id = $(this).attr('id');
    id = pred_id;
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
                $("#show_products").html(data).hide().fadeIn(1000);
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
                }
                $('.add_form').submit(add_cart_from_catalog);
            }
        });
    });
}

function load_products() {
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