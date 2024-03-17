from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.log_in, name='login'),
    path('api/logout', views.log_out, name='logout')
    path('api/stories', views.stories, name='stories'),
    path('api/stories/<int:story_key>/', views.delete_story, name='delete_story'),
]