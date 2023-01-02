from django.urls import path
from anki_web.users import views

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='create')
]
