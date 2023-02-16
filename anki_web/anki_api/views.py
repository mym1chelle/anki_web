from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from anki_web.anki_api.serializers import (
    CardsListSerializer,
    DetailCardSerializer,
    CreateCardSerializer,
    DeckListSerializer,
    StyleListSerializer,
    DeckStudyListSerializer,
    CreateDeckSerializer,
    CardsListStudySerializer,
)
from anki_web.cards.models import Cards
from anki_web.decks.models import Decks
from anki_web.styles.models import Styles
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from datetime import date
from random import randint


class StudyCardsAPIListPagination(PageNumberPagination):
    """Пагинация для вывода карточек по одной"""
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 30


class APIListPagination(PageNumberPagination):
    """Простая пагинация при просмотре всех карточек"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 30


class CardAPIShowUpdate(generics.RetrieveUpdateAPIView):
    """Вывод информации об выбранной карточке и обновление данной информации"""

    def get_queryset(self):
        queryset = Cards._default_manager.filter(id=self.kwargs.get('pk'))
        return queryset

    serializer_class = DetailCardSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class CardsListAPIView(generics.ListAPIView):
    """Выводит список всех карточек которые
    создал авторизированный пользователь"""
    def get_queryset(self):
        queryset = Cards._default_manager.filter(
            created_by=self.request.user.id
            )
        return queryset

    serializer_class = CardsListSerializer
    pagination_class = APIListPagination
    permission_classes = [
        IsAuthenticated,
    ]


class DecksListAPIView(generics.ListAPIView):
    """Выводит список колод которые создан авторизированный пользователь"""
    def get_queryset(self):
        queryset = Decks._default_manager.filter(
            created_by=self.request.user.id
            )
        return queryset

    serializer_class = DeckListSerializer
    pagination_class = APIListPagination
    permission_classes = [
        IsAuthenticated,
    ]


class StyleListAPIView(APIView):
    """Выводит список имеющихся стилей для вопроса и ответа"""
    def get(self, request, *args, **kwargs):
        styles = Styles._default_manager.all()
        serializer = StyleListSerializer(styles, many=True)
        return Response({'styles': serializer.data})

    permission_classes = [
        IsAuthenticated,
    ]


class CreateCardAPIView(generics.CreateAPIView):
    """Создание карточки"""
    serializer_class = CreateCardSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            created_by=request.user,
            random_num=randint(1, 2000)
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class CreateDeckAPIView(generics.CreateAPIView):
    """Создание колоды"""
    serializer_class = CreateDeckSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            created_by=request.user
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class CardsFilterListAPIView(generics.ListAPIView):
    """Выводит по одной карточке в выбранной колоде, где дата повторения
    не задана или меньше либо равна текущей дате"""
    def get_queryset(self):
        queryset = Cards._default_manager.filter(
            Q(review_date__isnull=True) | Q(review_date__lte=date.today())
        ).filter(deck=self.kwargs['id'])
        return queryset

    serializer_class = CardsListStudySerializer
    pagination_class = StudyCardsAPIListPagination
    permission_classes = [
        IsAuthenticated,
    ]


class StudyMainView(generics.ListAPIView):
    """Выводит список всех колод,
    где у карточек не задана дата повторения или
    дата повторения меньше либо равна текущей дате
    """
    def get_queryset(self):
        new = Count('cards', filter=Q(cards__review_date__isnull=True))
        old = Count('cards', filter=Q(cards__review_date__lte=date.today()))
        cards = Count('cards')
        queryset = Decks._default_manager.filter(
            created_by=self.request.user.id
        ).values(
            'id', 'name'
        ).annotate(new_cards=new).annotate(old_cards=old).annotate(
            all_cards=cards).filter(all_cards__gt=0)
        return queryset
    serializer_class = DeckStudyListSerializer

    permission_classes = [
        IsAuthenticated,
    ]
