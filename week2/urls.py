from django.urls import path

from . import views

app_name = "assistant"

urlpatterns = [
    path("api/", views.chat_api, name="chat_api"),
]
