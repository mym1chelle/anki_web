from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from anki_web import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('anki_web.anki_api.urls')),
    path('', views.MainPageView.as_view(), name='main_page'),
    path('login/', views.LoginUserView.as_view(next_page='main_page'), name='login'),
    path('logout/', LogoutView.as_view(next_page='main_page'), name='logout'),
    path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_done/', views.ResetPasswordDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.ResetPasswordConfirmView.as_view(),
         name='password_reset_confirm'
         ),
    path('password_reset_complete/', views.ResetPasswordCompleteView.as_view(),
         name='password_reset_complete'),
    path('users/', include('anki_web.users.urls')),
    path('decks/', include('anki_web.decks.urls')),
    path('cards/', include('anki_web.cards.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
