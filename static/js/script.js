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
		
		createTask : function(task_data) { 
			$.ajax({ type: "POST",   
		         url: "/create_task/",
		         async: true,
		         data: task_data,
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
		         success : function(text)
		         {
		        	alert(text);
		         }
			});
		},
		
		cancelTask: function(task_id) { 
			$.ajax({ type: "POST",   
		         url: "/cancel_task/" + task_id + "/",
		         async: true,
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
		         success : function(text)
		         {
		        	alert(text);
		         }
			});
		},
		
		getUserTasks: function(field_user_id) {
			$.ajax({ type: "GET",   
		         url: "/get_user_tasks/" + field_user_id + "/",
		         async: true,
		         beforeSend: function(xhr){ xhr.setRequestHeader("X-CSRFToken", util.getCookie('csrftoken'));},
		         success : function(text)
		         {
		        	alert(text);
		         }
			});
		},
}

$(document).ready(function(){
	var a = { 
		fuser : 1,
		lat : 12.1414,
		lon : 14.1414,
		name : "raz",
		desc : "opis",
	};
	var b = { id : 4};
	ajax.getUserTasks(1);
});
