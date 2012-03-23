from django.contrib import admin
from django.contrib.auth.models import User
from main_app.models import *

admin.site.register(Task)
admin.site.register(FieldUserProfile)
admin.site.register(Office)
admin.site.register(WorkDay)
admin.site.register(TaskState)
admin.site.register(TaskStateHistory)
