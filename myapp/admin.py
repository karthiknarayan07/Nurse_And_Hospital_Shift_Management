from django.contrib import admin

# Register your models here.
from .models import hospitalShiftDetails,AppliedNurses,User

admin.site.register(User)
admin.site.register(hospitalShiftDetails)
admin.site.register(AppliedNurses)

