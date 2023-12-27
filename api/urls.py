from django.urls import path

from api.views import accounts_views

app_name = 'api'

urlpatterns = [
    path('accounts/user/', accounts_views.UserView.as_view(), name='user_info'),
    path('accounts/activate/', accounts_views.ActivateView.as_view(), name='activate_user'),
]
