from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.RedirectUserProfile.as_view(),name="redirect_profile"),
    path('update_profile/',views.UpdateProfile.as_view(),name='update_profile'),
    path("<str:slug>/",views.AccountDetailView.as_view(),name="profile"),
]
