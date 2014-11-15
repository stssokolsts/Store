/**
 * Created by Евгений on 15.11.2014.
 */

function yandex_load () {
    ymaps.ready(init);
    var myMap,
        myPlacemark;

    function init() {
        myMap = new ymaps.Map("map", {
            center: [51.726593, 39.206052],
            zoom: 12
        });

        myPlacemark = new ymaps.Placemark([51.726593, 39.206052], {
            hintContent: 'Вкусный праздник',
            balloonContent: 'магазин "Вкусный праздник" - торты на заказ'
        });

        myMap.geoObjects.add(myPlacemark);
    }
}

function prepareDocument() {
    yandex_load();
}

$(document).ready(prepareDocument);
