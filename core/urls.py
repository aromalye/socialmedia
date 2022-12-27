from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('setting', views.setting, name='setting'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('upload_post', views.upload_post, name='upload_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('search', views.search, name='search'),
    path('follow/<int:user_id>/', views.follow, name='follow'),

]