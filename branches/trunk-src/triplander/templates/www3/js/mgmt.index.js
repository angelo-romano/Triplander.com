var is_center_set = false;

// show geomap popup
function showGeoMapPopup() {
	$("#geomap_popup").css("display","block");
	if(!is_center_set) {				    
		maps[0].checkResize();
		maps[0].setCenter(BaseJSSettings.mapCenter);
		is_center_set = true;
	}
}

// show addcity popup
function show_addcity() {
	$("#addcity_popup").css("display","block");
}

// process addcity
function process_addcity() {
	var cname    = $("#addcity_name").val();
	var ccountry = $("#addcity_country").val();
	$("#addcity_popup > div.loading").css('display','block');
	$.getJSON(BaseJSSettings.blueURL_city_add+"?name="+escape(cname)+"&country="+escape(ccountry), function(json){
		if(json.error == 0) {
			window.location.href = json.url;																			
		} else if(json.error == 1) { // city already existing
			window.location.href = json.url;
		} else if(json.error == 2) { // cannot be created
			$("#addcity_popup > div.loading").css('display','none');
			alert('City cannot be added. Does it actually exist?');
		}
	});

}

// activate a search form
function searchform_activate(which) {
	var whichOnes = ['city','country']
	for(var i=0; i < whichOnes.length; i++) {
		var curDiv = document.getElementById('search_box_'+whichOnes[i]);
		var curLink = document.getElementById('href_search_'+whichOnes[i]);
		if (whichOnes[i] == which) {
			curDiv.style.display = 'block';
			curLink.style.display = 'none';
		} else {
			curDiv.style.display = 'none';
			curLink.style.display = '';
		}
	}
	
	return;
}

// GeoMap procedures
var cur_markers = [];
var cur_markers_length = 0;
var map_maxmarkers = 30;
function refreshMapBoundary(oldLevel, newLevel) {
	var boundsSW = ""+maps[0].getBounds().getSouthWest().lat()+","+maps[0].getBounds().getSouthWest().lng();
	var boundsNE = ""+maps[0].getBounds().getNorthEast().lat()+","+maps[0].getBounds().getNorthEast().lng();
	$.getJSON(BaseJSSettings.blueURL_city_getPopular + boundsSW+";"+boundsNE, function(json){
		var j = 0;
		for(j in cur_markers) {
			if (cur_markers[j] != undefined ) {
				if (!maps[0].getBounds().containsLatLng(cur_markers[j].coords.getLatLng())) {
					maps[0].removeOverlay(cur_markers[j].coords);
					cur_markers[j] = undefined;
					cur_markers_length--;
				}
			}
		}
		var cm_base = cur_markers_length;
		var k = 0;
		j = cm_base;
		while (j < map_maxmarkers) {
			if (k < json.length) {
				var this_elem = json[k];
				if (cur_markers[this_elem.id] == undefined) {
					var marker = new GMarker(new GLatLng(this_elem.x,this_elem.y), {title: this_elem.name});
					marker.city_url = this_elem.url;
					GEvent.addListener(marker, "click", function() { location.href = this.city_url; });

					maps[0].addOverlay(marker);
					cur_markers[this_elem.id] = { name: this_elem.name, coords: marker, id: this_elem.id };
					cur_markers_length++;
					j++;
				}
				k = k + 1;
			} else {
				break;
			}
		}
	});
}
