from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from halls import views

urlpatterns = [

    # MAIN
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # AUTHENTICATION
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # GALLERIES
    path('gallery/create/', views.CreateHall.as_view(), name='create_gallery'),
    path('gallery/<int:pk>/', views.DetailHall.as_view(), name='detail_gallery'),
    path('gallery/<int:pk>/update/', views.UpdateHall.as_view(), name='update_gallery'),
    path('gallery/<int:pk>/delete/', views.DeleteHall.as_view(), name='delete_gallery'),

    # VIDEOS
    path('gallery/<int:pk>/add/', views.add, name='add'),
    path('video/search/', views.search_video, name='search_video'),
    path('video/<int:pk>/delete/', views.DeleteVideo.as_view(), name='delete_video'),
]

# if somebody does /static, mode to STATIC_ROOT
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
