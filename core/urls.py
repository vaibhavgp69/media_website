from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index' ),
    path('settings', views.settings, name='settings'),
    path('follow', views.follow, name='follow'),
    path('deletepost', views.deletepost, name='deletepost'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('commenting', views.commenting, name='commenting'),
    path('upload', views.upload, name='upload'),
    path('signup', views.signup, name='signup'),
    path('like-post', views.like_post, name='like-post'),
    path('dislike-post', views.dislike_post, name='dislike-post'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    
    
]
