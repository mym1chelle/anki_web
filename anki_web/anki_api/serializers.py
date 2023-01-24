from rest_framework import serializers
from anki_web.cards.models import Cards
from anki_web.decks.models import Decks
from anki_web.styles.models import Styles


class CardsListSerializer(serializers.ModelSerializer):
    deck = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Cards
        fields = [
            'id',
            'question',
            'answer',
            'deck',
        ]


class DetailCardSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Cards
        fields = [
            'question',
            'question_type',
            'answer',
            'answer_type',
            'style',
            'deck',
            'created_by',
            'random_num'
        ]


class CreateDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decks
        fields = [
            'name',
            'created_by'
        ]


class DeckListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Decks
        fields = [
            'id',
            'name'
        ]


class DeckStudyListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    new_cards = serializers.IntegerField(read_only=True)
    old_cards = serializers.IntegerField(read_only=True)


class StyleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Styles
        fields = [
            'id',
            'name'
        ]
