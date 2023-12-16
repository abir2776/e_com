from django.urls import path

from account.rest.views import register

urlpatterns = [
    path(
        "register",
        register.PublicUserRegistration.as_view(),
        name="user-registration",
    )
]
