from django.contrib import admin
from .models import Profile, User
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'country', 'date']
    search_fields = ['user', 'full_name', 'country']
    list_filter = ['date']
admin.site.register(Profile, ProfileAdmin)
admin.site.register(User)
