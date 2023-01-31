from rest_framework import generics
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
    CreateDeckSerializer
)
from anki_web.cards.models import Cards
from anki_web.decks.models import Decks
from anki_web.styles.models import Styles
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from datetime import date
from random import randint


class CardsAPIListPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 30


class CardAPIUpdate(APIView):
    """Вывод информации об выбранной карточке и обновление данной карточки"""
    def get(self, request, *args, **kwargs):
        card = Cards._default_manager.get(id=kwargs.get('pk'))
        if card.created_by.id == request.user.id:
            serializer = DetailCardSerializer(card)
            return Response(serializer.data)
        return Response({'errors': 'This user is not the creator of the selected object'})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'errors': 'Сould not find keywords argument "pk"'})
        try:
            instance = Cards._default_manager.get(id=pk)
        except:
            return Response({'errors': 'Object does not exists'})
        if instance.created_by.id == request.user.id:
            serializer = DetailCardSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'post': serializer.data})
        else:
            return Response({'errors': 'This user is not the creator of the selected object'})

    permission_classes = [
        IsAuthenticated,
    ]


class CardsListAPIView(generics.ListAPIView):
    """Выводит список всех карточек которые создал авторизированный пользователь"""
    def get_queryset(self):
        queryset = Cards._default_manager.filter(created_by=self.request.user.id)
        return queryset

    serializer_class = CardsListSerializer
    pagination_class = CardsAPIListPagination
    permission_classes = [
        IsAuthenticated,
    ]


class DecksListAPIView(APIView):
    """Выводит список колод которые создан авторизированный пользователь"""
    def get(self, request, *args, **kwargs):
        decks = Decks._default_manager.filter(created_by=request.user.id)
        serializer = DeckListSerializer(decks, many=True)
        return Response(serializer.data)

    permission_classes = [
        IsAuthenticated,
    ]


class StyleListAPIView(APIView):
    """Выводит список имеющихся стилей для вопроса и ответ"""
    def get(self, request, *args, **kwargs):
        styles = Styles._default_manager.all()
        serializer = StyleListSerializer(styles, many=True)
        return Response(serializer.data)

    permission_classes = [
        IsAuthenticated,
    ]


class CreateCardAPIView(APIView):
    """Создание карточки"""
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        print(request.data['question'])
        card = CreateCardSerializer(
            data={
                'question': request.data['question'],
                'question_type': request.data['question_type'],
                'answer': request.data['answer'],
                'answer_type': request.data['answer_type'],
                'style': request.data['style'],
                'deck': request.data['deck'],
                'created_by': request.user.id,
                'random_num': randint(1, 2000)
            }
        )
        if card.is_valid():
            card.save()
            return Response(status=201)
        else:
            return Response(status=424)


class CreateDeckAPIView(APIView):
    """Создание колоды"""
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        deck = CreateDeckSerializer(
            data={
                'name': request.data['name'],
                'created_by': request.user.id
            }
        )
        if deck.is_valid():
            deck.save()
            return Response(status=200)
        else:
            return Response(status=424)


class CardsStudyListView(generics.ListCreateAPIView):
    """Выводит список карточек в выбранной колоде, где дата повторения не задана или меньше либо равна текущей дате"""
    def get_queryset(self):
        queryset = Cards._default_manager.filter(
            Q(review_date__isnull=True) | Q(review_date__lte=date.today())
        ).filter(deck=self.kwargs['id'])
        return queryset

    serializer_class = CardsListSerializer
    pagination_class = CardsAPIListPagination
    permission_classes = [
        IsAuthenticated,
    ]


class StudyMainView(generics.ListAPIView):
    """Выводит список всех колод,
    где у карточек не задана дата повторения или дата повторения меньше либо равна текущей дате
    """
    def get_queryset(self):
        new = Count('cards', filter=Q(cards__review_date__isnull=True))
        old = Count('cards', filter=Q(cards__review_date__lte=date.today()))
        cards = Count('cards')
        queryset = Decks._default_manager.filter(
            created_by=self.request.user.id
        ).values(
            'id', 'name'
        ).annotate(new_cards=new).annotate(old_cards=old).annotate(all_cards=cards).filter(all_cards__gt=0)
        return queryset
    serializer_class = DeckStudyListSerializer

    permission_classes = [
        IsAuthenticated,
    ]
