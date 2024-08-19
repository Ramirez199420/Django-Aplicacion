from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# creando nuestras propias consultas o ORM, la class me va a crear una tabla de SQL que va a heredar desde models.Mdel que permite a Django crear la tabla y pongo los campso que quiero

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True) # para escribir textos mas largos
    created = models.DateTimeField(auto_now_add=True)# para saber la fecha y la hora en que fue creada la tarea
    datecompleted = models.DateTimeField(null=True, blank=True)# para marcar la fecha en que hizo la tarea o la tarea ya realizada o termin[o la tarea]
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #para cambiar el nombre de la tarea y no que me aparezca de manera tecnica como en el administrador que recibe self, como modelo a la propia class, tambie se le puede concatenar el usuario, que fue lo que puse
    def __str__(self):
        return self.title + '- by ' + self.user.username
