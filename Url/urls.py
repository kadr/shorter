from django.urls import path

from .views import UrlView

app_name = "url"
urlpatterns = [
    path('url/', UrlView.as_view()),
    path('url/<int:pk>', UrlView.as_view())
]