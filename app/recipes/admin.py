from django.contrib import admin
from recipes import models

admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
