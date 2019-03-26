from django.contrib import admin
from .models import *

# Register your models here.

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(User)
admin.site.register(Object)
admin.site.register(Records, RatingAdmin)
