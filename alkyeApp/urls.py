from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views 

urlpatterns = [
    path('posts/', views.postListCreate),
    path('postPagination/', views.postPagination),
    path('posts/<str:pk>/', views.postDetailsById),
    path('posts/<str:pk>/comments/', views.commentListCreate),
    path('posts/<str:pk>/like/', views.like_post),
    path('register/', views.register_user),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
