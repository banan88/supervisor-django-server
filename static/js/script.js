//utility functions

var util = {
	
	//cookie, csrf forgery mechanism from django
	getCookie : function(name) {
			        var cookieValue = null;
			        if (document.cookie && document.cookie != '') {
			            var cookies = document.cookie.split(';');
			            for (var i = 0; i < cookies.length; i++) {
			                var cookie = jQuery.trim(cookies[i]);
			                if (cookie.substring(0, name.length + 1) == (name + '=')) {
			                    cookieValue = decodeURIComponent(
			                    	cookie.substring(name.length + 1)
			                    );
			                    break;
			                }
			            }
			        }
			        return cookieValue;
		    	},

};

var googlemaps = {
	
	default_map : null,
		
    initMap : function(lat, lon) {
    	if (lat === undefined || lon === undefined) {
    		lat = 50.816327;
    		lon = 19.116479;
    	}
    	var center = new google.maps.LatLng(lat, lon);
    	  
	    var options = {
		    zoom : 15,
		    center : center,
		    mapTypeId : google.maps.MapTypeId.ROADMAP,
	    }
	    
	    default_map = new google.maps.Map($('#map').get(0), options);
	    
    },
    
    addMarker : function(lat, lon, image, text) {
    	
    	var center = new google.maps.LatLng(lat, lon);
	    var marker = new google.maps.Marker({
    	    position: center,
    	    map: default_map,
    	    icon: image,
    	    title: text,
    	});
    },
    
    chooseIcon : function() {
    	var task_state = $('#selectstate :selected').text();
    	switch(task_state){
    	case 'Aktywne':
    		var icon = '/static/img/current_marker.png'; 
    		return icon;
    	case 'Wykonane':
    		var icon = '/static/img/done_marker.png'; 
    		return icon;
    	case 'Oczekujące':
    		var icon = '/static/img/pending_marker.png'; 
    		return icon;
    	case 'Anulowane':
    		var icon = '/static/img/cancel_marker.png'; 
    		return icon;
    	}
    },
};

var ajax = {

   notifyOfSuccess : function() {
	   alert("pomyślnie zapisano zmiany!");
   },

   notifyOf500 : function() {
	   alert("Błąd serwera. Nie zapisano zmian!");
   },
		
    saveTask: function(onSuccess) {
        var task_id = window.location.pathname.split( '/' );
        task_id = task_id[task_id.length-2];
        var task_name = $('#inputname').val();
        var task_user = $('#inputuser').val();
        var task_state = $('#selectstate').val();
        var task_desc = $('#inputdesc').val();
        var task_lat = $('#inputlat').val();
        var task_lon = $('#inputlon').val();
        var task_data = {
            task_name : task_name,
            task_user : task_user,
            task_state : task_state,
            task_desc : task_desc,
            task_lat : task_lat,
            task_lon : task_lon,
        };
        $.ajax({ type: "POST",   
		         url: "/save_task/"+task_id+"/",
		         async: true,
		         data: task_data,
                 dataType: "json",
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));
                    if (xhr && xhr.overrideMimeType) {
                        xhr.overrideMimeType("application/j-son;charset=UTF-8");
                    }
                 },
		         success : function(return_data)
		         {
		        	 onSuccess(return_data);		  
		         },
                 statusCode: {
                    400: function() {
                        alert("niepoprawne wartości współrzędnych!\n Nie zapisano zmian!");
                    },
                    404: function() {
                        alert("takie zadanie nie istnieje. \nNie zapisano zmian!");
                    },
                    500: ajax.notifyOf500
                 }
			});
    }
};

$(document).ready(function () {
	var lat = $('#inputlat').val();
	var lon = $('#inputlon').val();
	var name = $('#inputname').val();
	
    googlemaps.initMap(lat, lon);
    googlemaps.addMarker(lat, lon, googlemaps.chooseIcon(), name);
    
  $('#edit_task').click(function(){
    $('#task-form :input ').not('#inputsuper').removeAttr('disabled');
  });
  
  $('#cancel_change').click(function(){
	  history.go(0);
	  $('#task-form :input').attr('disabled', 'true');
	  });
  
  $('#save_task').click(function(){
	if($('#inputname').is(':disabled')==false) {
		$('#task-form :input').attr('disabled', 'true');
	    lat = $('#inputlat').val();
		lon = $('#inputlon').val();
		name = $('#inputname').val();
		googlemaps.initMap(lat, lon);
		googlemaps.addMarker(lat, lon, googlemaps.chooseIcon(), name);
	    ajax.saveTask(ajax.notifyOfSuccess);
	}
	else
		alert("brak zmian do zapisania!");
  });
  
  $('#refresh').click(function(){
	  var lat = $('#inputlat').val();
  	  var lon = $('#inputlon').val();
  	  name = $('#inputname').val();
	  googlemaps.initMap(lat, lon);
	  googlemaps.addMarker(lat, lon, googlemaps.chooseIcon(), name);
  });
});
