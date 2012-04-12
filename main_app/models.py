# -*- coding: utf8

from django.db import models
from django.contrib.auth.models import User
import datetime

#profil pracownika terenowego powiazany z obiektem usera (nadzorca ma jest po prostu userem, bez profilu)

class FieldUserProfile(models.Model): 
    user = models.OneToOneField(User)
    last_latitude = models.FloatField(blank = True, null = True)
    last_longitude = models.FloatField(blank = True, null = True)
    imei_number = models.CharField(max_length = 30, blank = True, null = True)
    phone_numer = models.CharField(max_length = 20, blank = True, null = True)
    home_adress = models.CharField(max_length = 50, blank = True, null = True)
    sync_time = models.DateTimeField(blank = True, null = True)

STATES = (
        ('3', 'done'),
        ('2', 'current'),
        ('1', 'pending'),
        ('0', 'cancelled'),
        )


class Task(models.Model):
    fieldUser = models.ForeignKey(User, related_name = 'fielduser_set') 
    latitude = models.FloatField()
    longitude = models.FloatField()
    state = models.CharField(choices = STATES, max_length = 1)
    name = models.CharField(max_length = 30)
    description = models.TextField()
    creation_time = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    finish_time = models.DateTimeField(blank = True, null = True)
    start_time = models.DateTimeField(blank = True, null = True)
    supervisor = models.ForeignKey(User, related_name = 'user_set')                                        #nadzorca
    version = models.IntegerField(default = 0)                   #na podstawie tej wartosci przeprowadzana jest synchronizacja

    def updateTaskHistory(self, task_pk, new_state, was_content_edited, user, timestamp, tag):
        updatedHistory = TaskStateHistory(task = task_pk,
                                          state_changed_to = new_state,
                                          content_edited = was_content_edited,
                                          user_editor = user,
                                          change_time = timestamp,
                                          change_description = tag)
        updatedHistory.save()

    def save(self, *args, **kwargs):
        self.version += 1
        super(Task, self).save(*args, **kwargs)
        #przy tworzeniu zadania nie trzeba osobno wywolywac updateTaskHistory - hack do testow w django admin
        if self.version == 1:
            savedTaskInstance = Task.objects.get(pk = self.pk)
            self.updateTaskHistory(savedTaskInstance, self.state, True,
                self.supervisor, datetime.datetime.now(),
                u"zadanie zostalo utworzone przez użytkownika \"" + self.supervisor.username + "\"")
    
    def __unicode__(self):
        return self.name + " " + str(self.latitude) + " " + str(self.longitude)



class TaskStateHistory(models.Model):
    task = models.ForeignKey(Task)
    state_changed_to =  models.CharField(choices = STATES, max_length = 1)
    content_edited = models.BooleanField(default = False) #czy poza stanem cos sie zmienilo
    user_editor = models.ForeignKey(User) #kto wykonal zmiane
    change_time = models.DateTimeField();
    change_description = models.CharField(max_length = 50)
    change_latitude = models.FloatField(null = True)
    change_longitude = models.FloatField(null = True)

 
class WorkDay(models.Model):
    fieldUser = models.ForeignKey(User)
    day = models.DateField()
    start = models.DateTimeField()
    finish = models.DateTimeField()

class UserLocation(models.Model):
    user = models.ForeignKey(User)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()