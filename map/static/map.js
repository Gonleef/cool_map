$(document).ready(function() {
      var container = document.getElementById('popup');
      var content = document.getElementById('popup-content');
      var closer = document.getElementById('popup-closer');


      /**
       * Create an overlay to anchor the popup to the map.
       */
      var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
        element: container,
        autoPan: true,
        autoPanAnimation: {
          duration: 250
        }
      }));


      /**
       * Add a click handler to hide the popup.
       * @return {boolean} Don't follow the href.
       */
      closer.onclick = function() {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
      };


      /**
       * Create the map.
       */
      var map = new ol.Map({
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          })
        ],
        overlays: [overlay],
        target: 'map',
        view: new ol.View({
          center: ol.proj.fromLonLat([60.61, 56.82]),
          zoom: 13
        })
      });


      /**
       * Add a click handler to the map to render the popup.
       */
      map.on('click', function(evt) {
        var coordinate = evt.coordinate;
        var data = ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326');
        var lon = data.substring(data[0]);
        var lat = data.substring(data[1]);
        $.get("http://nominatim.openstreetmap.org/reverse?format=json&lat="+lat+"&lon=" + lon + "&addressdetails=1", function(data) {
            console.log(data);
        });
		content.innerHTML =
				'<input type="hidden" name="lon" value="'+lon+'"/>' +
				'<input type="hidden" name="lat" value="'+lat+'"/>' +
				'<button id="send">Написать отзыв</button>';
        overlay.setPosition(coordinate);
       $("#send").click(function(){
            var coordinate = evt.coordinate;
            var data = ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326').toString();
            var lat = data.substring(data.indexOf(",") + 1,data.length);
            var lon = data.substring(0, data.indexOf(","));


          });
      });



});