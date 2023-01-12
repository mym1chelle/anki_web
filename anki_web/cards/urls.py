from django.urls import path
from anki_web.cards import views

app_name = 'cards'
urlpatterns = [
    path('<int:pk>/update/', views.UpdateCardView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteCardView.as_view(), name='delete'),
    path('<int:card_id>/answer/<int:quality>/', views.check_answer, name='answer'),
    path('<int:pk>', views.DetailCardView.as_view(), name='show_card'),
]
