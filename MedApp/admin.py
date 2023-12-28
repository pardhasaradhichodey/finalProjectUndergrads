from django.contrib import admin
from .models import DiagnosticCentre,Hospital,Tests,TestsOffered,User,SlotBookAndReport,Doctor
admin.site.register(DiagnosticCentre)
admin.site.register(Hospital)
admin.site.register(Tests)
admin.site.register(TestsOffered)
admin.site.register(User)
admin.site.register(SlotBookAndReport)
admin.site.register(Doctor)
# Register your models here.
