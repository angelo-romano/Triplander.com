var active_form = 'connection';
var base_url = 'http://127.0.0.1:8000/';

function searchform_connection_chooseFrom() {
	searchform_getcityinfo();
	searchform_populate_destinations();
	var fromElem = $('searchfield_connection_from');
	var toBlockElem = $('searchfieldset_connection_to');
	var toElem = $('searchfield_connection_to');
	if (fromElem.value == '') {
		toBlockElem.style.display = 'none';
		return;
	}
	toElem.options[0].selected = true;
	for(var i = 1; i < toElem.length; i++) {
		if (toElem.options[i].value != fromElem.value) {
			toElem.options[i].style.display = '';
			toElem.options[i].selected = false;
		} else {
			toElem.options[i].style.display = 'none';
			toElem.options[i].selected = false;
		}
	}
	toBlockElem.style.display = 'inline';
	return;
}

function searchform_activate(which) {
	var whichOnes = ['city','country']
	for(var i=0; i < whichOnes.length; i++) {
		var curDiv = $('search_box_'+which);
		var curLink = $('href_search_'+which);
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

function searchform_getcityinfo() {
	var serviceURL = base_url+'wbserv/2/'+$('searchfield_connection_from').value;
	var ajaxReq = new Ajax(serviceURL,{
		method: 'get',
		evalScripts: true,
		onComplete: function(){
			var req = ajaxReq.response['text'];
			var respObj = Json.evaluate(req);
			euromap_set_marker(respObj['city'],respObj['latitude'],respObj['longitude']);
			
		}
	}).request();
}

function searchform_populate_destinations() {
	var serviceURL = base_url+'wbserv/1/'+$('searchfield_connection_from').value;
	
	var ajaxReq = new Ajax(serviceURL,{
		method: 'get',
		evalScripts: true,
		onComplete: function(){
			var req = ajaxReq.response['text'];
			var dObj = $('searchfield_connection_to');
			var baseOffset = 4;
			
			for(var i=dObj.length-1; i>=baseOffset; i--)
				dObj.remove(i);
				
			var respObj = Json.evaluate(req);
			
			for(var k in respObj) {
				var c = respObj[k]['fields'];
				if($defined(c) && $defined(c['short_name']) && $defined(c['code_alt'])) {
					var newOpt = document.createElement('option');
					newOpt.text = decodeURI(c['short_name'])+' ['+c['code_alt']+']';
					newOpt.value = c['code_alt'];
					dObj.add(newOpt,null);
				}
			}
		}
	}).request();
}

function enable_autocomplete() {
}
