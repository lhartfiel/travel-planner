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
from django.conf.urls import url
from django.contrib import admin
from django.db import router
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from travel_group import views

from accommodations.views import AccommodationListView, AccommodationDetailView, AccommodationCreateView, \
    AccommodationEditView, AccommodationDeleteView, AccommodationListTravelGroupView
from travel_users.views import UserLoginView, ProfileView, ProfileEditView, UserSignupView, UserSignupSuccessView, \
    UserLogoutView, ChecklistAllView
from travel_group.views import TravelGroupListView, TravelGroupSingleView, TravelGroupCreateView, SightseeingEditView, \
    RestaurantEditView, MessageEditView, SightseeingAddView, SightseeingDeleteView, RestaurantDeleteView, \
    RestaurantAddView, TravelerAccommodationListView, MessageAddView, TravelGroupChecklistView, \
    TravelGroupChecklistEditView, TravelGroupChecklistList, TravelGroupChecklistDelete, ChecklistViewSet, \
    MessageDeleteView, TravelGroupEditView, TravelGroupImage, InviteFormView, TravelGroupAddTraveler, \
    TravelGroupRemoveUserView, TravelGroupInvitePendingView, TravelGroupInviteSentView
from travel_transportation.views import TransportationEditView, TransportationCreateView, TransportationListView, \
    TransportationDetailView, TransportationDeleteView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'checklist', ChecklistViewSet)


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('accommodation-list/<username>', AccommodationListView.as_view(), name="accommodation_list"),
    path('accommodation-list/for/<username>/<int:pk>', AccommodationListTravelGroupView.as_view(),
         name="accommodation_list_travelgroup"),
    path('accommodation-detail/<slug:username>/<pk>', AccommodationDetailView.as_view(), name="accommodation_detail"),
    path('accommodation-create', AccommodationCreateView.as_view(), name="accommodation_create"),
    path('accommodation-edit/<pk>', AccommodationEditView.as_view(), name="accommodation_edit"),
    path('accommodation-delete/<pk>', AccommodationDeleteView.as_view(), name="accommodation_delete"),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<slug:username>/', ProfileView.as_view(), name="profile"),
    path('edit/<slug:username>/', ProfileEditView.as_view(), name='edit'),
    path('checklists/for/<slug:username>/', ChecklistAllView.as_view(), name="checklists"),
    path('signup/<int:travel_group_id>/', UserSignupView.as_view(), name="signup"),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('signup/success/', UserSignupSuccessView.as_view(), name="signup_success"),
    path('travel-group/create/', TravelGroupCreateView.as_view(), name="travel_group_create"),
    path('travel-group/invite-sent/<int:pk>/', TravelGroupInviteSentView.as_view(), kwargs={'recipient': ''},
         name="travel_group_invite_sent"),
    path('travel-group/invite-pending/<int:pk>/<slug:username>', TravelGroupInvitePendingView.as_view(),
         name="travel_group_invite_pending"),
    path('travel-group/remove-user/<int:pk>/<slug:username>', TravelGroupRemoveUserView.as_view(),
         name="travel_group_remove_user"),
    path('travel-group-invite-form/<int:pk>/<slug:username>', InviteFormView.as_view(), name="invite-form"),
    path('travel-group/edit/<int:pk>', TravelGroupEditView.as_view(), name="travel_group_edit"),
    path('travel-group/sightseeing-edit/<int:pk>/', SightseeingEditView.as_view(), name="sightseeing_edit"),
    path('travel-group/sightseeing-add/<int:pk>', SightseeingAddView.as_view(), name="sightseeing_add"),
    path('travel-group/sightseeing-delete/<int:pk>', SightseeingDeleteView.as_view(), name="sightseeing_delete"),
    path('travel-group/restaurant-edit/<int:id>', RestaurantEditView.as_view(), name="restaurant_edit"),
    path('travel-group/restaurant-delete/<int:id>', RestaurantDeleteView.as_view(), name="restaurant_delete"),
    path('travel-group/restaurant-add/<int:id>', RestaurantAddView.as_view(), name="restaurant_add"),
    path('travel-group/<int:id>/message-edit/', MessageEditView.as_view(), name="message_edit"),
    path('travel-group/message-add/<int:id>', MessageAddView.as_view(), name="message_add"),
    path('travel-group/message-delete/<int:pk>', MessageDeleteView.as_view(), name="message_delete"),
    path('travel-group/checklist-add/<int:id>/<slug:username>', TravelGroupChecklistView.as_view(), name="travel_checklist_create"),
    path('travel-group/checklist-edit/<int:pk>/<slug:username>', TravelGroupChecklistEditView.as_view(), name="travel_checklist_edit"),
    path('travel-group/checklist-update', TravelGroupChecklistEditView.as_view(), name="travel_checklist_update"),
    path('travel-group/checklist-delete/<int:pk>/<slug:username>', TravelGroupChecklistDelete.as_view(), name="travel_checklist_delete"),
    path('travel-group/checklist-list/<int:id>/<slug:username>', TravelGroupChecklistList.as_view(), name="travel_checklist_list"),
    path('travel-group/for/<slug:username>/', TravelGroupListView.as_view(), name="travel_group_index"),
    path('travel-group/accommodations/<int:pk>/<slug:username>', TravelerAccommodationListView.as_view(), name="traveler_accommodation"),
    path('travel-group/<int:pk>/', TravelGroupSingleView.as_view(), name="travel_group_single"),
    path('travel-group/<int:pk>/add-traveler', TravelGroupAddTraveler.as_view(), name="add_traveler"),
    path('transportation-list/<slug:username>', TransportationListView.as_view(), name="transportation_list"),
    path('transportation-detail/<slug:username>/<int:pk>', TransportationDetailView.as_view(), name="transportation_detail"),
    path('transportation-create/<int:pk>', TransportationCreateView.as_view(), name="transportation_create"),
    path('transportation-edit/<int:pk>', TransportationEditView.as_view(), name="transportation_edit"),
    path('transportation-delete/<int:pk>', TransportationDeleteView.as_view(), name="transportation_delete"),
    url(r"^invitations/", include("pinax.invitations.urls", namespace="pinax_invitations")),
    path('djrichtextfield/', include('djrichtextfield.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-unsplash/', TravelGroupImage.as_view(), name="unsplash"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)

