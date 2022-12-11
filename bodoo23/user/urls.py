from django.urls import path
from . import views
# from .views import *
from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('login', Login.as_view(), name='login'),
    path('signup', Signup.as_view(), name='signup'),
    path('user-detail/', UserDetail.as_view(), name='user-detail'),
    path('global-var/', GlobalVarView.as_view(), name='global-var'),
    path('special-user/', SpecialUserView.as_view(), name='special-user'),
]
