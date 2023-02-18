from django.urls import path
from anki_web.users import views

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='create'),
    path('user/', views.show_user, name='show_user')
]
