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
		

}

$(document).ready(function(){
	var a = { 
		fuser : 2,
		lat : 12.1414,
		lon : 14.1414,
		name : "raz",
		desc : "opis",
	};
	var b = { id : 4};
	//ajax.getUserTasks(2, function(data){alert(data['8'].created);});
	//ajax.editTaskState(7, function(data){alert(data);}, 2)
	ajax.che
});
