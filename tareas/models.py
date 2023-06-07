from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tareas(models.Model):
    title = models.CharField(max_length=100) #tipo texto
    description = models.TextField(blank=True) # tipo memo
    created = models.DateField(auto_now_add=True) # tipo fecha, con autoagregado de la fecha
    datecompleted = models.DateTimeField(null=True, blank=True) # tipo fecha, puede estar vacio, porque es fecha de finalización
    important = models.BooleanField(default=False) # tipo boolean
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Tipo foreign key, si elimina usuario elimina las tareas
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username