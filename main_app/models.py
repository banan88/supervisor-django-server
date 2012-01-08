from django.db import models
from django.contrib.auth.models import User

#biuro, nie wiem czy bedzie uzywane, ew przy rozbudowie

class Office(models.Model):
    name = models.CharField(max_length = 50, blank = False, null = True)
    adress = models.CharField(max_length = 50, blank = True, null = True)
    phone_number = models.CharField(max_length = 20, blank = True, null = True)   

#profil pracownika terenowego powiazany z obiektem usera (nadzorca ma jest po prostu userem, bez profilu)

class FieldUserProfile(models.Model): 
    user = models.OneToOneField(User)
    last_latitude = models.FloatField(blank = True, null = True)
    last_longitude = models.FloatField(blank = True, null = True)
    imei_number = models.CharField(max_length = 30, blank = True, null = True)
    phone_numer = models.CharField(max_length = 20, blank = True, null = True)
    home_adress = models.CharField(max_length = 50, blank = True, null = True)
    office = models.ForeignKey(Office)
    sync_time = models.DateTimeField(blank = True, null = True)
#zadanie

class Task(models.Model):                                                       #klienci korzystaja w swoich bazach z id obiektow tej klasy
    STATES = (
              ('3', 'done'),                                                    #wykonane
              ('2', 'current'),                                                 #obecnie wykonywane
              ('1', 'pending'),                                                 #w kolejce u pracownika terenowego
              ('0', 'cancelled'),                                               #anulowane przez nadzorce                                             #nieprzypisane pracownikowi
              )
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
    last_synced = models.DateTimeField(blank = True, null = True)
    #importance = models.IntegerField(default = 0)
    
    def save(self, *args, **kwargs):
         self.version += 1
         super(Task, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name + " " + str(self.latitude) + " " + str(self.longitude)
    
 


    
