from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 1. Admin Panel (Backend Control)
    path('admin/', admin.site.urls),

    # 2. Main Exam App (Sare paths yahan se connect hain)
    path('', include('exam.urls')), 

    # 3. Built-in Authentication (Login, Logout, Password Reset)
    # Isse django.contrib.auth.urls ke sare features active ho jayenge
    path('accounts/', include('django.contrib.auth.urls')),

    # 4. Extra: Logout Redirect Fix (Optional par zaruri)
    # Agar logout karne pe error aaye toh ye line help karegi
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]