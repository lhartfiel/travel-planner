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
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from travel_users.views import UserLoginView, ProfileView, ProfileEditView, UserSignupView, UserSignupSuccessView, UserLogoutView
from travel_group.views import TravelGroupListView, TravelGroupSingleView, TravelGroupCreateView, SightseeingEditView, \
    RestaurantEditView, MessageEditView, SightseeingAddView, SightseeingDeleteView
from travel_transportation.views import TransportationEditView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<username>/', ProfileView.as_view(), name="profile"),
    path('edit/<username>/', ProfileEditView.as_view(), name='edit'),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('signup/success/', UserSignupSuccessView.as_view(), name="signup_success"),
    path('travel-group/create/', TravelGroupCreateView.as_view(), name="travel_group_create"),
    path('travel-group/sightseeing-edit/<pk>/', SightseeingEditView.as_view(), name="sightseeing_edit"),
    path('travel-group/sightseeing-add/<pk>', SightseeingAddView.as_view(), name="sightseeing_add"),
    path('travel-group/sightseeing-delete/<pk>', SightseeingDeleteView.as_view(), name="sightseeing_delete"),
    path('travel-group/<id>/restaurant-edit/', RestaurantEditView.as_view(), name="restaurant_edit"),
    path('travel-group/<id>/message-edit/', MessageEditView.as_view(), name="message_edit"),
    path('travel-group/for/<username>/', TravelGroupListView.as_view(), name="travel_group_index"),
    path('travel-group/<pk>/', TravelGroupSingleView.as_view(), name="travel_group_single"),
    path('travel-group/<pk>/transportation-edit', TransportationEditView.as_view(), name="transportation_edit"),
    path('djrichtextfield/', include('djrichtextfield.urls'))
]
