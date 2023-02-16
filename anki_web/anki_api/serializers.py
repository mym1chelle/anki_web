from rest_framework import serializers
from anki_web.cards.models import Cards
from anki_web.decks.models import Decks
from anki_web.styles.models import Styles


class CardsListSerializer(serializers.ModelSerializer):
    """Сериализация вывода всех карточек выбранного пользователя"""
    deck = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Cards
        fields = [
            'id',
            'question',
            'answer',
            'deck',
        ]


class CardsListStudySerializer(serializers.ModelSerializer):
    """Сериализация вывода отфильтрованных карточек по одной"""
    style = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Cards
        fields = [
            'id',
            'question',
            'question_type',
            'answer',
            'answer_type',
            'style'
        ]


class DetailCardSerializer(serializers.ModelSerializer):
    """Сериализация обновляемых данных в карточке"""
    class Meta:
        model = Cards
        fields = [
            'id',
            'easiness',
            'interval',
            'repetitions',
            'review_date'
        ]


class CreateCardSerializer(serializers.ModelSerializer):
    """Сериализации данных при добавлении новой карточки"""
    class Meta:
        model = Cards
        fields = [
            'question',
            'question_type',
            'answer',
            'answer_type',
            'style',
            'deck',
        ]


class CreateDeckSerializer(serializers.ModelSerializer):
    """Сериализация данных при создании колоды"""
    class Meta:
        model = Decks
        fields = [
            'name'
        ]


class DeckListSerializer(serializers.ModelSerializer):
    """Сериализация для списка колод"""
    class Meta:
        model = Decks
        fields = [
            'id',
            'name'
        ]


class DeckStudyListSerializer(serializers.Serializer):
    """Сериализация данных о выбранное колоде и количестве
    в ней карточек, удовлетворяющих условиям"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    new_cards = serializers.IntegerField(read_only=True)
    old_cards = serializers.IntegerField(read_only=True)


class StyleListSerializer(serializers.ModelSerializer):
    """Сериализация данных при выводе списка стилей"""
    class Meta:
        model = Styles
        fields = [
            'id',
            'name'
        ]
