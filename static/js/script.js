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

var mapsutil = {
	
	default_map : null,
	
	markersArray : [],

	polylinesArray: [],
	
	clearPolilines: function() {
		for(i in mapsutil.polylinesArray){
			mapsutil.polylinesArray[i].setMap(null);		
		}
	},

	deleteOverlays : function() {
		if (mapsutil.markersArray) {
			for (i in mapsutil.markersArray) {
				mapsutil.markersArray[i].setMap(null);
		    }
			mapsutil.markersArray.length = 0;
		}
	},
		
    initMap : function(lat, lon) {
    	if ((lat === undefined || lon === undefined) || (parseFloat(lat) === NaN || parseFloat(lon) === NaN)) {
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
    
    showLocation : function(lat, lon, image, text) {
    	
    	var center = new google.maps.LatLng(lat, lon);
	    var marker = new google.maps.Marker({
    	    position: center,
    	    map: default_map,
    	    icon: image,
    	    title: text,
    	});
	    mapsutil.markersArray.push(marker);
	    default_map.panTo(marker.getPosition());
	    var infowindow = new google.maps.InfoWindow();
	    google.maps.event.addListener(marker, 'click', (function(marker, text) {
	        return function() {
			infowindow.setContent('Szerokość: ' + lat + '<br>Długość:' + lon);
	        infowindow.open(default_map, marker);
	        }
	      })(marker));
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
    	default:
    		var icon = '/static/img/me.png'; 
			return icon;
    	}
    },
   
    
    drawPath : function(array) {
	mapsutil.clearPolilines();
    	mapsutil.deleteOverlays();
    	if(array.length > 0) {
	    	mapsutil.initMap(array[0]['lat'], array[0]['lon']);
	    	var img = mapsutil.chooseIcon();
	    	var polylinePoints =[];
		for (elem in array){
	    		var marker = new google.maps.Marker({
	    	        position: new google.maps.LatLng(parseFloat(array[elem].lat),  parseFloat(array[elem].lon)),
	    	        icon: img,
	    	        map: default_map,
	    	        title: array[elem].timestamp,
	    	        content: elem,
	    	      });
	    		mapsutil.markersArray.push(marker);
	    		polylinePoints.push(marker.getPosition());
	    		var infowindow = new google.maps.InfoWindow();
	    		google.maps.event.addListener(marker, 'click', (function(marker, text) {
	    		        return function() {
	    				infowindow.setContent(text);
	    		        infowindow.open(default_map, marker);
	    		        }
	    		      })(marker, marker.position + " <br>" + marker.title));
	    	}
	    	var Polyline_Path = new google.maps.Polyline({
	    		path: polylinePoints,
	    		strokeColor: "#4b8df9",
	    		strokeOpacity: 0.8,
	    		strokeWeight: 2
	    		});
	    		Polyline_Path.setMap(default_map);
		mapsutil.polylinesArray.push(Polyline_Path);
    	}
    },
    	
    	showUsers: function(array) {
        	if(array.length > 0) {
    	    	//mapsutil.initMap(array[0]['lat'], array[0]['lon']);
    	    	var img = '/static/img/me.png';
    	    	var lat = default_map.getCenter().lat();
    	        var lng = default_map.getCenter().lng();
    	        var R = 6371;
    	        var distances = [];
    	        var closest = -1;
    		for (elem in array){
    			
    	    		var marker = new google.maps.Marker({
    	    	        position: new google.maps.LatLng(parseFloat(array[elem].lat),  parseFloat(array[elem].lon)),
    	    	        icon: img,
    	    	        map: default_map,
    	    	        title: array[elem].user,
    	    	        content: elem,
    	    	      });
    	    		mapsutil.markersArray.push(marker);
    	    		var infowindow = new google.maps.InfoWindow();
    	    		google.maps.event.addListener(marker, 'click', (function(marker, text) {
    	    		        return function() {
    	    				infowindow.setContent(text);
    	    		        infowindow.open(default_map, marker);
    	    		        }
    	    		      })(marker, marker.position + " <br>" + marker.title + " <br>" + array[elem].time));
    	    		var mlat = parseFloat(array[elem].lat);
    	            var mlng = parseFloat(array[elem].lon);
    	            var dLat  = mapsutil.rad(mlat - lat);
    	            var dLong = mapsutil.rad(mlng - lng);
    	            var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    	                Math.cos(mapsutil.rad(lat)) * Math.cos(mapsutil.rad(lat)) * Math.sin(dLong/2) * Math.sin(dLong/2);
    	            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    	            var d = R * c;
    	            distances[elem] = d;
    	            if ( closest == -1 || d < distances[closest] ) {
    	                closest = elem;
    	            }
    	    	}
    		$("#closest").html(array[closest].user);
    		$("#closest").click(function() {
    			$("#id_fieldUser > option").each(function(){
    				if(this.text === $("#closest").html())
    					$(this).attr('selected', 'selected');
    			});
    		});
    		//alert(array[closest].user);
        	}
    },
    
    rad : function(x) {return x*Math.PI/180;},

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
                        xhr.overrideMimeType("application/json;charset=UTF-8");
                    }
                 },
		         success : function(return_data)
		         {
		        	 onSuccess(return_data);		  
		         },
                 statusCode: {
                    400: function() {
                        alert("podano niepoprawne wartości!\n Nie zapisano zmian!");
                        window.location.reload( false );
                    },
                    404: function() {
                        alert("takie zadanie nie istnieje. \nNie zapisano zmian!");
                    },
                    500: ajax.notifyOf500
                 }
			});
    },
    
    loadPath: function(from, to, onSuccess) {
    	var time = {
    			from : from,
    			to : to,
    	}
    	var id = window.location.pathname.split( '/' );
        id = id[id.length-2];
    	$.ajax({ type: "POST",   
	         url: "/load_path/"+id+"/",
	         async: true,
	         data: time,
            dataType: "json",
	         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));
               if (xhr && xhr.overrideMimeType) {
                   xhr.overrideMimeType("application/json;charset=UTF-8");
               }
            },
	         success : function(return_data)
	         {
	        	 onSuccess(return_data);		  
	         },
            statusCode: {
               400: function() {
                   alert("niepoprawne wartości czasu!\n Nie zapisano zmian!");
               },
               404: function() {
                   alert("takie zadanie nie istnieje. \nNie zapisano zmian!");
               },
               500: ajax.notifyOf500
            }
		});
    },
    
    loadUsersLocations: function(onSuccess) {
    	$.ajax({ type: "POST",   
	         url: "/load_user_locations/",
	         async: true,
	         data: {},
            dataType: "json",
	         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));
               if (xhr && xhr.overrideMimeType) {
                   xhr.overrideMimeType("application/json;charset=UTF-8");
               }
            },
	         success : function(return_data)
	         {
	        	 onSuccess(return_data);		  
	         },
            statusCode: {
               400: function() {
                   alert("niepoprawne uprawnienia!");
               },
               404: function() {
                   alert("brak danych!");
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
	
	if($('.dateinputon').length>0)
		$('.dateinputon').datepicker($.datepicker.regional['pl']);
	
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

	if($('.dateinputon').length>0){
		var lat = $('#inputlat').html();
		var lon = $('#inputlon').html();
	}
	else {
		var lat = $('#inputlat').val();
		var lon = $('#inputlon').val();
	}
		
	var name = $('#inputname').val();
	
	if($('#map').length >0) {
	    mapsutil.initMap(lat, lon);
	    mapsutil.clearPolilines();
	    mapsutil.deleteOverlays();
	    if($("#refresh").hasClass('task_users')) {
			  mapsutil.showLocation(lat, lon, mapsutil.chooseIcon(), name);
			  ajax.loadUsersLocations(mapsutil.showUsers);
			  
		  }
		  else {
			  mapsutil.showLocation(lat, lon, mapsutil.chooseIcon(), name);
		  }
	}
  $('#edit_task').click(function(){
    $('#task-form :input ').not('#inputsuper').removeAttr('disabled');
  });
  
  $('#cancel_change').click(function(){
	  window.location.reload()
	  $('#task-form :input').attr('disabled', 'true');
	  });
  
  $('#save_task').click(function(){
	if($('#inputname').is(':disabled')==false) {
		$('#task-form :input').attr('disabled', 'true');
	    lat = $('#inputlat').val();
		lon = $('#inputlon').val();
		name = $('#inputname').val();
		mapsutil.initMap(lat, lon);
    		mapsutil.clearPolilines();		
		mapsutil.deleteOverlays();
		mapsutil.showLocation(lat, lon, mapsutil.chooseIcon(), name);
	    ajax.saveTask(ajax.notifyOfSuccess);
	}
	else
		alert("brak zmian do zapisania!");
  });
  
  $('#refresh').click(function(){
	  var lat = $('#inputlat').val();
  	  var lon = $('#inputlon').val();
  	  name = $('#inputname').val();
	  mapsutil.initMap(lat, lon);
	  mapsutil.clearPolilines();
	  mapsutil.deleteOverlays();
	  if($(this).hasClass('task_users')) {
		  mapsutil.showLocation(lat, lon, mapsutil.chooseIcon(), name);
		  ajax.loadUsersLocations(mapsutil.showUsers);
		  
	  }
	  else {
		  mapsutil.showLocation(lat, lon, mapsutil.chooseIcon(), name);
	  }
  });
  
  $('#searchuser').keyup(function(event) {
	  	alert('ok');
		if($(this).val().length > 3)
			util.suggestUsers();
		else if($(this).val().length == 0)
			$("#usersuggest").hide();
	});
  
  $('#searchsuper').blur(function(){
		setTimeout(function(){
			$("#usersuggest").hide();
	    }, 250);
	});
  
  $('#location').click(function() {
	  mapsutil.clearPolilines();
	  mapsutil.deleteOverlays();
	  mapsutil.showLocation(lat, lon, mapsutil.chooseIcon(), name);
	  $(this).addClass('btn-success');
	  $('#show_path').addClass('disabled');
	  $('#path').removeClass('btn-success');
	  $('.dateinputon').attr('disabled', 'disabled');
  });
  
  $('#path').click(function() {
	  $(this).addClass('btn-success');
	  $('#location').removeClass('btn-success');
	  $('#show_path').removeClass('disabled');
	  $('.dateinputon').removeAttr('disabled');
  });
  
  $('#show_path').click(function() {
	  ajax.loadPath($('#datefrom').val(), $('#dateto').val(), mapsutil.drawPath);
  });

});
