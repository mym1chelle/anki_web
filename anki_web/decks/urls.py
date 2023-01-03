from django.urls import path
from anki_web.decks import views
from anki_web.cards.views import CreateCardView, ListCardsView, upload_file, ListCardsDayView, show_answer, delete_select_cards, delete_all_cards

app_name = 'decks'
urlpatterns = [
    path('', views.ListDecksView.as_view(), name='decks'),
    path('create/', views.CreateDeckView.as_view(), name='create'),
    path('<int:pk>/select/', delete_select_cards, name='select'),
    path('<int:pk>/delete_all_cards/', delete_all_cards, name='delete_all'),
    path('<int:pk>/create/', CreateCardView.as_view(), name='create_card'),
    path('<int:pk>/upload/', upload_file, name='upload'),
    path('<int:pk>/cards/', ListCardsView.as_view(), name='cards'),
    path('<int:pk>/learn/', ListCardsDayView.as_view(), name='learn'),
    path('<int:pk>/delete/', views.DeleteDeckView.as_view(), name='delete'),
    path('<int:card_id>/answer/', show_answer, name='answer'),
]
