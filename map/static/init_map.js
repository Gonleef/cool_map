(function () {
    var map = new ol.Map({target: 'map'});
    map.addLayer(new ol.layer.Tile({source: new ol.source.OSM()}));
        view: new ol.View({
            center: ol.proj.fromLonLat([60.61, 56.82]),
            zoom: 13
        })
    });
})();