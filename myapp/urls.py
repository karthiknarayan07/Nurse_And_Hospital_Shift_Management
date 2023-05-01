from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),

    path('register_nurse',views.register_nurse,name="register_nurse"),
    path('register_hospital',views.register_hospital,name="register_hospital"),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),
    path('hospital',views.hospital,name="hospital"),
    path('nurse',views.nurse,name="nurse"),
    path('hospital/openshifts/<int:shiftID>',views.openshifts,name="openShifts"),
    
]