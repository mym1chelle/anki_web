from django.urls import path, include, re_path
from anki_web.anki_api.views import (
    CardsListAPIView,
    CreateCardAPIView,
    DecksListAPIView,
    StyleListAPIView,
    CardsStudyListView,
    StudyMainView,
    CreateDeckAPIView,
    CardAPIUpdate
)

urlpatterns = [
    path('auth-session/', include('rest_framework.urls')),
    path('auth-token/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('cards/', CardsListAPIView.as_view()),
    path('styles/', StyleListAPIView.as_view()),
    path('decks/', DecksListAPIView.as_view()),
    path('deck/<int:id>/cards', CardsStudyListView.as_view()),
    path('cards/create/', CreateCardAPIView.as_view()),
    path('decks/create/', CreateDeckAPIView.as_view()),
    path('study/', StudyMainView.as_view()),
    path('cards/<int:pk>/', CardAPIUpdate.as_view())
]