// show/hide editcity
function editcity_show() {
    $('#editcity_popup').css('display','block');
    geodjango.map1.checkResize();
    geodjango.map1.setCenter(
                      new GLatLng($('#editcity_latitude').val(),$('#editcity_longitude').val()),
                      editview_gmapzoom);
}
function editcity_gmap_onclick(overlay, latlng) {
    if (latlng) { 
        var vLat = parseFloat(parseFloat(latlng.lat()).toFixed(5));
        var vLng = parseFloat(parseFloat(latlng.lng()).toFixed(5));
        latlng = new GLatLng(vLat,vLng);
        var myHtml = "Coordinates: <br /><strong>"+vLat+","+vLng+"</strong>";
        if (editview_gmarker == null) {
            editview_gmarker = new GMarker(latlng,{
                                                   icon: new GIcon(G_DEFAULT_ICON,"/static/images/marker_std_alternate.png")});
            geodjango.map1.addOverlay(editview_gmarker);
        } else {
            editview_gmarker.setLatLng(latlng);
        }
        geodjango.map1.setCenter(latlng, editview_gmapzoom)
        geodjango.map1.openInfoWindow(latlng, myHtml);
        $('#editcity_latitude').val(vLat);
        $('#editcity_longitude').val(vLng);
    }
}
// change latitude/longitude
// process editcity
function editcity_process() {
	$("#editcity_popup > div.loading").css('display','block'); // loading...
    var edit_vals = {
        id         : BaseJSSettings.cityID,
        name       : $("#editcity_name").val(),
        country    : $("#editcity_country").val(),
        localname  : $("#editcity_localname").val(),
        population : $("#editcity_population").val(),
        wikiname   : $("#editcity_wikiname").val(),
        x          : $("#editcity_latitude").val(),
        y          : $("#editcity_longitude").val(),
        rerank     : ($("#editcity_rerank").val() == 'yes' ? '1' : '0'),
    };
    
    $.post(BaseJSSettings.blueURL_city_edit, edit_vals, function(json){
        if(json.error == 0) {
            window.location.href=json.url;
        } else {
        	$("#editcity_popup > div.loading").css('display','none');
        	alert('Unexpected error.');
        }
    },"json");
}