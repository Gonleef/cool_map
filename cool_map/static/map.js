$(document).ready(function() {
        debugger;
      var container = document.getElementById('popup');
      var content = document.getElementById('popup-content');
      var closer = document.getElementById('popup-closer');


      closer.onclick = function() {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
      };

        map.on('singleclick', function(evt) {
        var coordinate = evt.coordinate;
				var data = ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326').toString();
				var lat = data.substring(data.indexOf(",") + 1,data.length);
				var lon = data.substring(0, data.indexOf(","));
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
		$.get("http://nominatim.openstreetmap.org/reverse?format=json&lat="+lat+"&lon=" + lon + "&addressdetails=1", function(data) {
			console.log(data);
		});

	  });
      });

     

});
