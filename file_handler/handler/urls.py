from django.urls import path

from handler import views


urlpatterns = [
    path('file/', views.FileListView.as_view()),
    path('file/<int:pk>', views.FileDetailsView.as_view()),
]