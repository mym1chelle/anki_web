from rest_framework import serializers
from anki_web.cards.models import Cards


class CardsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cards
        fields = [
            'id',
            'question',
            'deck',
        ]


class DetailCardSerializer(serializers.ModelSerializer):

    deck = serializers.SlugRelatedField('name', read_only=True)
    style = serializers.SlugRelatedField('name', read_only=True)
    created_by = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = Cards
        exclude = (
            'easiness',
            'interval',
            'repetitions',
            'review_date',
            'random_num',
        )


class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = [
            'question',
            'answer',
            'style',
            'created_by',
            'deck'
        ]