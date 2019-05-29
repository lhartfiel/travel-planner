"""travel_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from travel_users import views
from django.views.generic import TemplateView
from travel_users.views import ProfileView, ProfileEditView, UserSignupView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls'), name='login'),
    path('profile/', ProfileView.as_view()),
    path('edit/<username>/', ProfileEditView.as_view(), name='edit'),
    path('signup/', UserSignupView.as_view(), name="signup"),
]
