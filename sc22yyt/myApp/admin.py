from django.contrib import admin
from .models import Author, Story, Agency

# Register your models here.

admin.site.register (Author)
admin.site.register (Story)
admin.site.register (Agency)