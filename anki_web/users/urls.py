from django.urls import path
from anki_web.users import views

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='create'),
    path('user/', views.show_user, name='show_user'),
    path('<int:pk>/update/', views.UpdateUserInfoView.as_view(), name='update'),
    path('change_password/', views.change_password, name='password')
]
