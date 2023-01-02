from django.urls import path
from anki_web.decks import views
from anki_web.cards.views import CreateCardView, ListCardsView, upload_file, ListCardsDayView, show_answer

app_name = 'decks'
urlpatterns = [
    path('', views.ListDecksView.as_view(), name='decks'),
    path('create/', views.CreateDeckView.as_view(), name='create'),
    path('<int:pk>/create/', CreateCardView.as_view(), name='create_card'),
    path('<int:pk>/upload/', upload_file, name='upload'),
    path('<int:pk>/cards/', ListCardsView.as_view(), name='cards'),
    path('<int:pk>/learn/', ListCardsDayView.as_view(), name='learn'),
    path('<int:card_id>/answer/', show_answer, name='answer'),
]
