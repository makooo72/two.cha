from django.urls import path, include
from . import views


urlpatterns = [
    path('registration', views.RegistrationView.as_view(), name="registration"),
    path('', include('django.contrib.auth.urls')),
    path('profile', views.UserDetailView.as_view(), name="profile"),
    path('profile/edit', views.EditProfileView.as_view(), name="edit_profile"),
    path('profile/save', views.SaveChangesProfileView.as_view(), name="edit_profile"),
]