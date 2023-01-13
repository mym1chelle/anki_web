from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from anki_web import views
from django.conf.urls.static import static
from django.conf import settings
from anki_web.cards.views import CardsListAPIView, DetailCardAPIView, CreateCardAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/cards/<int:id>/', DetailCardAPIView.as_view()),
    path('api/v1/cards/', CardsListAPIView.as_view()),
    path('api/v1/create/', CreateCardAPIView.as_view()),
    path('', views.MainPageView.as_view(), name='main_page'),
    path('login/', views.LoginUserView.as_view(next_page='main_page'), name='login'),
    path('logout', LogoutView.as_view(next_page='main_page'), name='logout'),
    path('users/', include('anki_web.users.urls')),
    path('decks/', include('anki_web.decks.urls')),
    path('cards/', include('anki_web.cards.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns