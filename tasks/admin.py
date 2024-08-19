from django.contrib import admin
from .models import Task


# para agregar la fecha de creacion
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )# readblabla, es para solo lectura y donde lo quiero ver en pantalla

# Register your models here.
# para cambiar nuestra tabla o desde el admin web qu es el panel de administrador o del 
admin.site.register(Task, TaskAdmin)
