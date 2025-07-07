from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import AcceptGasOrderView, ActiveOrderView, AllGasOrdersView, AvailableGasOrdersView, DriverRegisterViewsss, GasOrderCreateView, OrderHistoryView, UserProfileUpdateView, UserRegistrationView, sriverLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('orders/create/', GasOrderCreateView.as_view(), name='create-order'),
    path('drivers/registersss/', DriverRegisterViewsss.as_view(), name='driver-register'),
    path('drivers/orders/all/', AllGasOrdersView.as_view(), name='all-orders'),
    path('drivers/login/', sriverLoginView.as_view(), name='driver-login'),
    path('drivers/orders/available/', AvailableGasOrdersView.as_view(), name='available-gas-orders'),
    path('driver/orders/<int:order_id>/accept/', AcceptGasOrderView.as_view()),
    path('orders/active/', ActiveOrderView.as_view(), name='user_active-order'),
    path('orders/history/', OrderHistoryView.as_view(), name='user_order-history'),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),


]
