from django.contrib import admin

from .models import AdmissionToken


class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'isActive', 'createdTime', 'updatedTime']
    list_filter = ['isActive']


admin.site.register(AdmissionToken, TokenAdmin)
