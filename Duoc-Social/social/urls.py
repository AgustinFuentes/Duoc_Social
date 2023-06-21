from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
  path('', views.feed, name='feed'),
  path('profile/', views.profile, name='profile'),
  path('profile/<str:username>/', views.profile, name='profile'),
  path('register/', views.register, name='register'),
  path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
  path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
  path('post/', views.post, name='post'),
  path('vote/<int:post_id>/', views.vote_post, name='vote_post'),
  path('follow/<str:username>/', views.follow, name='follow'),
  path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
  path('create_conversation/<str:username>/', views.create_conversation, name='create_conversation'),
  path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
  path('send_message/<int:conversation_id>/', views.send_message, name='send_message'),
  path('conversations/', views.conversation_list, name='conversation_list'),
  path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
  path('terms/', views.terms, name='terms'),
  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)