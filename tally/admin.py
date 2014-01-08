from django.contrib import admin
from tally.models import Archive

class ArchiveAdmin (admin.ModelAdmin):
    list_display = ('name', 'slug', 'pattern', 'resolution', 'retention')

admin.site.register(Archive, ArchiveAdmin)
