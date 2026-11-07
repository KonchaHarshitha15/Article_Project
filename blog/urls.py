from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.PostListView.as_view(),name='home'),

    path('logout/',views.logout_page,name='logout'),

    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),

    path('register/',views.register_view,name='register'),

    path('profile/',views.profile_view,name='profile'),

    path('create/',views.PostCreateView.as_view(),name='create'),

    path('<int:pk>/detail/',views.PostDetailView.as_view(),name='detail'),

    path('about/',views.about_view,name='about'),

    path('latest_post/',views.LatestPostListView.as_view(),name='latest_post'),

    path('<int:pk>/update/',views.PostUpdateView.as_view(),name='update'),

    path('<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete'),

    path('<str:username>/posts/',views.UserPostListView.as_view(),name='posts'),

    path('services/',views.services_view,name='services'),


]