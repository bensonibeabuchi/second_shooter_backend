from django.contrib import admin
from .models import *

# Register your models here.

class ShotListAdmin(admin.ModelAdmin):
    list_display = ["shot_description", "shot_type", "is_done"]
    list_editable = ["shot_type", "is_done"]
    list_filter = ["shot_type", "is_done"]


admin.site.register(ShotList, ShotListAdmin )

class ConsentFormAdmin(admin.ModelAdmin):
    list_display = [ "subject_name", "agency_name", "photographer_name", "date" ]
    list_editable = ["agency_name", "photographer_name" ]
    list_filter = ["agency_name", "photographer_name", "subject_name", "date"]

admin.site.register(ConsentForm, ConsentFormAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project_name", "user", ]
    list_filter = ["project_name"]
    prepopulated_fields = {"slug": ("project_name",)}
    

admin.site.register(Project, ProjectAdmin)