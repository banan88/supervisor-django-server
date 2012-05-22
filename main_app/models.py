# -*- coding: utf8

from django.db import models
from django.contrib.auth.models import User
from django import forms
import datetime

#profil pracownika terenowego powiazany z obiektem usera (nadzorca ma jest po prostu userem, bez profilu)

class FieldUserProfile(models.Model): 
    user = models.OneToOneField(User, verbose_name="Konto użytkownika")
    last_latitude = models.DecimalField(blank = True, null = True, max_digits=11, decimal_places=8, verbose_name="Ostatnia szerokość geograficzna")
    last_longitude = models.DecimalField(blank = True, null = True, max_digits=11, decimal_places=8, verbose_name="Ostatnia długość geograficzna")
    imei_number = models.CharField(max_length = 30, blank = True, null = True, verbose_name="Numer IMEI telefonu")
    phone_numer = models.CharField(max_length = 20, blank = True, null = True, verbose_name="Kontaktowy numer telefonu")
    home_adress = models.CharField(max_length = 50, blank = True, null = True, verbose_name="Adres domowy")
    sync_time = models.DateTimeField(blank = True, null = True, verbose_name="Czas ostatniej synchronizacji")

    class Meta:
        verbose_name = "Profil użytkownika mobilnego"
        verbose_name_plural = "Profile użytkowników mobilnych"

    def __unicode__(self):
        return self.user.username + ", lokalizacja: (%s, %s)" %(str(self.last_latitude or "brak") , str(self.last_latitude or "brak"))

STATES = (
        ('3', 'Wykonane'),
        ('2', 'Aktywne'),
        ('1', 'Oczekujące'),
        ('0', 'Anulowane'),
        )


class Task(models.Model):
    fieldUser = models.ForeignKey(User, related_name = 'fielduser_set', verbose_name='użytkownik terenowy')
    latitude = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="szerokość geograficzna")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="długość geograficzna")
    state = models.CharField(choices = STATES, max_length = 1, verbose_name="stan")
    name = models.CharField(max_length = 30, verbose_name="nazwa")
    description = models.TextField(verbose_name="opis")
    creation_time = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    finish_time = models.DateTimeField(blank = True, null = True)
    start_time = models.DateTimeField(blank = True, null = True)
    supervisor = models.ForeignKey(User, related_name = 'user_set')                                        #nadzorca
    version = models.IntegerField(default = 0)                   #na podstawie tej wartosci przeprowadzana jest synchronizacja

    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"

    def updateTaskHistory(self, new_state, was_content_edited, user, timestamp, tag):
        updatedHistory = TaskStateHistory(task = self,
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
            self.updateTaskHistory(self.state, True,
                self.supervisor, datetime.datetime.now(),
                u"zadanie zostalo utworzone")
    
    def __unicode__(self):
        return self.name + " " + str(self.latitude) + " " + str(self.longitude)



class TaskStateHistory(models.Model):
    task = models.ForeignKey(Task)
    state_changed_to =  models.CharField(choices = STATES, max_length = 1)
    content_edited = models.BooleanField(default = False) #czy poza stanem cos sie zmienilo
    user_editor = models.ForeignKey(User) #kto wykonal zmiane
    change_time = models.DateTimeField();
    change_description = models.CharField(max_length = 50)
    change_latitude = models.DecimalField(null = True, max_digits=11, decimal_places=8) #coodinates where change was made
    change_longitude = models.DecimalField(null = True, max_digits=11, decimal_places=8)

    class Meta:
        verbose_name = "Historia zmian zadania"
        verbose_name_plural = "Historie zmian zadań"
 
class WorkDay(models.Model):
    fieldUser = models.ForeignKey(User)
    day = models.DateField()
    start = models.DateTimeField()
    finish = models.DateTimeField()

    class Meta:
        verbose_name = "Dzień pracy"
        verbose_name_plural = "Kalendarze czasu pracy"

class UserLocation(models.Model):
    user = models.ForeignKey(User)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name = "Lokalizacja użytkownika"
        verbose_name_plural = "Lokalizacje użytkowników"


#### FORMS ####

class TaskForm(forms.ModelForm):
    latitude = forms.DecimalField(max_value = 85, min_value = -85, widget=forms.TextInput(attrs={'id':'inputlat',}))
    longitude = forms.DecimalField(max_value = 180, min_value = -180, widget=forms.TextInput(attrs={'id':'inputlon',}))
    state = forms.ChoiceField(choices = STATES, widget=forms.Select( attrs={'id':'selectstate',}))
    latitude.label = "Szerokość geograficzna"
    longitude.label = "Długość geograficzna"
    
    class Meta:
        model = Task
        fields = ['name','fieldUser', 'state', 'description', 'latitude', 'longitude']

  