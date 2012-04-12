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

var ajax = {
		/*
		 * onSuccess - funkcja przyjmujaca dane odebrane poprzez ajax
		 * 
		 * task_data is a json object, for example:
		 * 
		 * { 
			fuser : 2,
			lat : 12.1414,
			lon : 14.1414,
			name : "raz",
			desc : "opis",
		   };
		 * 
		 */

        notifyOfSuccess : function() {
            alert("pomyślnie zapisano zmiany!");
        },

        notifyOf500 : function() {
            alert("Błąd serwera. Nie zapisano zmian!");
        },

		createTask : function(task_data, onSuccess) { 
			$.ajax({ type: "POST",   
		         url: "/create_task/",
		         async: true,
		         data: task_data,
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
		         success : function(return_data)
		         {
		        	 onSuccess(return_data);
		         }
			});
		},
		
		editTaskState: function(task_id, onSuccess, state) { 
			$.ajax({ type: "GET",   
		         url: "/edit_task_state/" + task_id + '/' + state + '/',
		         async: true,
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
		         success : function(return_data)
		         {
		        	 onSuccess(return_data);
		         }
			});
		},
		
		/*
		 * without state returns all tasks for that user
		 * state = models.Task.STATES
		 */ 
		
		getUserTasks: function(field_user_id, onSuccess, opt_state) {
			//if opt_state not supplied -> target url is without last param
			opt_state = typeof(opt_state) 
			!= 'undefined' ? opt_state : '';
			
			$.ajax({ type: "GET",   
		         url: "/get_user_tasks/" + field_user_id + '/' + opt_state + '/',
		         async: true,
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
		         success : function(return_data)
		         {
		        	 onSuccess(return_data);
		         }
			});
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
                        alert("takie zadanie nie istnieje");
                    },
                    500: ajax.notifyOf500
                 }
			});
    }
};

$(document).ready(function () {
  $('#edit_task').click(function(){
    $('#task-form :input ').not('#inputsuper').removeAttr('disabled');
  });
  $('#save_task').click(function(){
    $('#task-form :input').attr('disabled', 'true');
    ajax.saveTask(ajax.notifyOfSuccess);
  });
});
