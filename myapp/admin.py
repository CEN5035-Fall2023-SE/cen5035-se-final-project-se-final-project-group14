from django.contrib import admin
from .models import TaApplicant, DepartmentStaff, Instructor, TACoimmitteeMember

# Register your models with the admin site
admin.site.register(TaApplicant)
admin.site.register(DepartmentStaff)
admin.site.register(Instructor)
admin.site.register(TACoimmitteeMember)
