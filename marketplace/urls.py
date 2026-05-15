from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.home, name='home'),
    path('artworks/', views.artwork_list, name='artwork_list'),
    path('artworks/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('artworks/<int:pk>/bid/', views.submit_bid, name='submit_bid'),
    path('artworks/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('sellers/<int:pk>/', views.seller_detail, name='seller_detail'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('bids/', views.bid_list, name='bid_list'),
    path('bids/<int:pk>/finalize/', views.finalize_bid, name='finalize_bid'),
    path(
        'bids/<int:pk>/finalize/<str:step>/',
        views.finalize_bid,
        name='finalize_bid_step',
    ),
    path('accounts/register/', views.register, name='register'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
]
