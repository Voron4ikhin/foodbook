from django.urls import path
from .views import (
    my_profile_view,
    invites_received_view,
    profiles_list_view,
    invite_profiles_list_view,
    ProfileDetailView,
    ProfileListView,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
    my_friends_view,
    users_friends,
)


app_name = 'profile'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('myfriends/', my_friends_view, name='my-friends-view'),
    path('frineds/<slug>/', users_friends, name='users-friends'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('myinvites/accept/', accept_invitation, name='accept-invite'),
    path('myinvites/reject/', reject_invitation, name='reject-invite'),
    path('<slug>/', ProfileDetailView.as_view(), name='profiles-detail-view'),
]