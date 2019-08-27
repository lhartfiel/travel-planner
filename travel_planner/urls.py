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
from django.conf import settings
from django.conf.urls.static import static

from accommodations.views import AccommodationListView, AccommodationDetailView, AccommodationCreateView, \
    AccommodationEditView, AccommodationDeleteView
from travel_users.views import UserLoginView, ProfileView, ProfileEditView, UserSignupView, UserSignupSuccessView, UserLogoutView
from travel_group.views import TravelGroupListView, TravelGroupSingleView, TravelGroupCreateView, SightseeingEditView, \
    RestaurantEditView, MessageEditView, SightseeingAddView, SightseeingDeleteView, RestaurantDeleteView, \
    RestaurantAddView, TravelerAccommodationListView, MessageAddView
from travel_transportation.views import TransportationEditView, TransportationCreateView, TransportationListView, \
    TransportationDetailView, TransportationDeleteView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('accommodation-list/<username>', AccommodationListView.as_view(), name="accommodation_list"),
    path('accommodation-detail/<username>/<pk>', AccommodationDetailView.as_view(), name="accommodation_detail"),
    path('accommodation-create', AccommodationCreateView.as_view(), name="accommodation_create"),
    path('accommodation-edit/<pk>', AccommodationEditView.as_view(), name="accommodation_edit"),
    path('accommodation-delete/<pk>', AccommodationDeleteView.as_view(), name="accommodation_delete"),
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
    path('travel-group/restaurant-edit/<int:id>', RestaurantEditView.as_view(), name="restaurant_edit"),
    path('travel-group/restaurant-delete/<int:id>', RestaurantDeleteView.as_view(), name="restaurant_delete"),
    path('travel-group/restaurant-add/<int:id>', RestaurantAddView.as_view(), name="restaurant_add"),
    path('travel-group/<id>/message-edit/', MessageEditView.as_view(), name="message_edit"),
    path('travel-group/message-add/<int:id>', MessageAddView.as_view(), name="message_add"),
    path('travel-group/for/<username>/', TravelGroupListView.as_view(), name="travel_group_index"),
    path('travel-group/accommodations/<pk>/<username>', TravelerAccommodationListView.as_view(), name="traveler_accommodation"),
    path('travel-group/<pk>/', TravelGroupSingleView.as_view(), name="travel_group_single"),
    path('transportation-list/<username>', TransportationListView.as_view(), name="transportation_list"),
    path('transportation-detail/<username>/<pk>', TransportationDetailView.as_view(), name="transportation_detail"),
    path('transportation-create/<pk>', TransportationCreateView.as_view(), name="transportation_create"),
    path('transportation-edit/<pk>', TransportationEditView.as_view(), name="transportation_edit"),
    path('transportation-delete/<pk>', TransportationDeleteView.as_view(), name="transportation_delete"),
    path('djrichtextfield/', include('djrichtextfield.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
