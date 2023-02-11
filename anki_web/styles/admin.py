from django.contrib import admin
from anki_web.styles.models import Styles


@admin.register(Styles)
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['name', 'created_at']
