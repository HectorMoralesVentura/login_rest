from django.urls import path
from api.views import UserList

urlpatterns = [
    path('user/',UserList.as_view(), name = 'user_list'),
]