"""
URL configuration for mainproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('about', views.about),
    path('contact', views.contact),
    path('doctor', views.doctor),
    path('', views.index),
    path('appointment', views.appointment),
    path('treatment', views.treatment),
    path('signup', views.signup),
    path('adminhome', views.adminhome),
    path('login', views.login),
    path('logout', views.logout,name='logout'),
    path('userhome', views.userhome),
    path('treatment2', views.treatment2),
    path('doctor2', views.doctor2),
    path('adddoctor', views.adddoctor),
    path('addtreatment', views.addtreatment),
    path('message', views.message),
    path('managedoctor', views.managedoctor),
    # path('update', views.update),
    path('form', views.normal),
    path('modelform', views.modelform),
    path('update_form/<int:d>', views.update_form),
    path('delete/<int:d>',views.delete_doctor),
    path('delete_message/<int:d>',views.delete_message),
    path('managetreatment', views.managetreatment),
    path('appointmentapprove/', views.appointmentapprove, name='appointmentapprove'),
    path('doctorhome/', views.doctorhome, name='doctorhome'),
    path('doctorprofile', views.doctorprofile),
    path('form2', views.normal2),
    # path('modelform2', views.modelform2),
    path('update_form2/<int:d>', views.update_form2),
    path('delete_treatment/<int:d>', views.delete_treatment),
    path('myappointment', views.myappointment),
    path('payment', views.payment),
    path('success', views.success),
    path('set_time_slot/', views.set_time_slot, name='set_time_slot'),
    path('forgot', views.forgot_password),
    path('reset_password/<token>', views.reset_password),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
