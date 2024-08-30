from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostUserListView.as_view(), name='post_list'),
    path('newpost/', views.post_create, name='post_create'),
    path('like/<int:pk>/', views.post_like, name='post_like'),
]
