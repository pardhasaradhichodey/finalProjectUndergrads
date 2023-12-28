from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('addBene',views.addBene,name='addBene'),
    path('logout',views.logout,name='logout'),
    path('DiagnosticCenter',views.DiagnosticCenter,name='DiagnosticCenter'),
    path('DiagnosticCenterDashboard',views.DiagnosticCenterDashboard,name='DiagnosticCenterDashboard'),
    path('addTests',views.addTests,name='addTests'),
    path('Dclogout',views.Dclogout,name='Dclogout'),
    path('TestBook',views.TestBook,name='TestBook'),
    path('TestBookSuccess',views.TestBookSuccess,name='TestBookSuccess'),
    path('UploadReport/<int:SlotId>',views.UploadReport,name='UploadReport'),
    path('viewReport',views.viewReport,name='viewReport'),
    path('BookWard',views.BookWard,name='BookWard'),
    path('DoctorConsultation/<int:SlotId>',views.DoctorConsultation,name='DoctorConsultation'),
    path('DoctorConsultConfirm',views.DoctorConsultConfirm,name='DoctorConsultConfirm')
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)