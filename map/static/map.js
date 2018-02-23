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
	    console.log(data);
        var lon = data[0];
        var lat = data[1];
        var xhr = new XMLHttpRequest();
        console.log(lon);
        xhr.open('GET', '/api/place/v1/geodecoding?lon=' + lon + '&lat=' + lat , true);
            xhr.send();
            xhr.onreadystatechange = function() {
                if (xhr.readyState !== 4) return;
                if (xhr.status === 200) {
                    var data = JSON.parse(xhr.response.toString());
                    console.log(data);
                    content.innerHTML = '<form action="choose" method="post"><input type="hidden" name="place_id" value="'+data.id+'"/>' + '<hr>' +
                    '<button id="send">Написать отзыв</button></form>';
                    overlay.setPosition(coordinate);

                }

            }
            });



});