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
		    	
	suggestUsers : function() {
		$.ajax({ type: "POST",   
	         url: "/getusersuggestions/",
	         async: false,
	         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
	         data: {'q':$("#inputuser").val()},
	         success : function(json)
	         {
	        	 if( !($.isEmptyObject(json))){
	        		 $('#usersuggest').empty().show();
		        	 for(var key in json){
		        		 $('#usersuggest').append('<a class = "user_suggestion" href=\"#\">' +json[key]+ '</a><br>');
		        	 }
	        	 }
	        	 else
	        		 $('#usersuggest').hide();
	         }
		});
	},
	
	suggestSuper : function() {
		$.ajax({ type: "POST",   
	         url: "/getsupersuggestions/",
	         async: false,
	         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
	         data: {'q':$("#inputsuper").val()},
	         success : function(json)
	         {
	        	 if( !($.isEmptyObject(json))){
	        		 $('#supersuggest').empty().show();
		        	 for(var key in json){
		        		 $('#supersuggest').append('<a class = "super_suggestion" href=\"#\">' +json[key]+ '</a><br>');
		        	 }
	        	 }
	        	 else
	        		 $('#supersuggest').hide();
	         }
		});
	},
	
	suggestNames : function() {
		$.ajax({ type: "POST",   
	         url: "/getnamesuggestions/",
	         async: false,
	         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
	         data: {'q':$("#inputname").val()},
	         success : function(json)
	         {
	        	 if( !($.isEmptyObject(json))){
	        		 $('#namesuggest').empty().show();
	        		 for(var key in json){
	        			 $('#namesuggest').append('<a class = "name_suggestion" href=\"#\">' +json[key]+ '</a><br>');
	        		 } 
	        	 }
	        	 else
	        		 $('#namesuggest').hide();
	         }
		});
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
	
	$('body').on('click', 'a.user_suggestion', function() {
	    var txt = $(this).text();
	    $("#inputuser").val(txt);
	});
	
	$('body').on('click', 'a.super_suggestion', function() {
	    var txt = $(this).text();
	    $("#inputsuper").val(txt);
	});
	
	$('body').on('click', 'a.name_suggestion', function() {
	    var txt = $(this).text();
	    $("#inputname").val(txt);
	});

	
	if($(this).val() === "0")
		$(".dateinput").removeAttr('disabled');
	
	
	if ($('.dateinput').length) {
		$( ".dateinput" ).datepicker($.datepicker.regional['pl']);
		$(".dateinput").attr('disabled', 'true');

		if($('#selecttime').val() == "0") {
			$(".dateinput").removeAttr('disabled');
		}	
		
		$("#selecttime").change(function(){
			if($(this).val() === "0")
				$(".dateinput").removeAttr('disabled');
			else
				$(".dateinput").attr('disabled', 'true');
		});
	}
	
	$('#inputname').keyup(function(event) {
		if($(this).val().length > 3)
			util.suggestNames();
		else if($(this).val().length == 0)
			$("#namesuggest").hide();
	});
	
	$('#inputname').blur(function(){
		setTimeout(function(){
			$("#namesuggest").hide();
	    }, 250);
	});
	
	$('#inputuser').keyup(function(event) {
		if($(this).val().length > 3)
			util.suggestUsers();
		else if($(this).val().length == 0)
			$("#usersuggest").hide();
	});
	
	$('#inputuser').blur(function(){
		setTimeout(function(){
			$("#usersuggest").hide();
	    }, 250);
	});
	
	$('#inputsuper').keyup(function(event) {
		if($(this).val().length > 3)
			util.suggestSuper();
		else if($(this).val().length == 0)
			$("#supersuggest").hide();
	});
	
	$('#inputsuper').blur(function(){
		setTimeout(function(){
			$("#supersuggest").hide();
	    }, 250);
	});

	
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
