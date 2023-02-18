from django.urls import path
from anki_web.cards import views

app_name = 'cards'
urlpatterns = [
    path('<int:pk>/update/', views.UpdateCardView.as_view(), name='update'),
    path('delete/', views.DeleteAllCardsView.as_view(), name='delete_all'),
    path('<int:pk>/delete/', views.DeleteCardView.as_view(), name='delete'),
    path('<int:card_id>/answer/', views.check_answer, name='answer'),
    path('<int:pk>', views.DetailCardView.as_view(), name='show_card'),
    path('all/', views.AllCardsView.as_view(), name='all_cards'),
    path('select/', views.delete_select_cards, name='select'),
    path('<download/', views.download_file, name='download')
]
