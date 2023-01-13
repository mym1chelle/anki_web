from django.urls import path
from anki_web.anki_api.views import CardsListAPIView, DetailCardAPIView, CreateCardAPIView

urlpatterns = [
    path('cards/<int:id>/', DetailCardAPIView.as_view()),
    path('cards/', CardsListAPIView.as_view()),
    path('create/', CreateCardAPIView.as_view()),
]