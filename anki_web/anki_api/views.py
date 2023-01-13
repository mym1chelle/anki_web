# импорт для DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from anki_web.anki_api.serializers import CardsListSerializer, DetailCardSerializer, CreateCardSerializer
from anki_web.cards.models import Cards


# попытка разобраться с DRF

class CardsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cards = Cards.objects.all()[:20]
        serializer = CardsListSerializer(cards, many=True)
        return Response(serializer.data)


class DetailCardAPIView(APIView):
    def get(self, request, *args, **kwargs):
        card = Cards.objects.get(id=kwargs.get('id'))
        serializer = DetailCardSerializer(card)
        return Response(serializer.data)


class CreateCardAPIView(APIView):
    def post(self, request, *args, **kwargs):
        card = CreateCardSerializer(data=request.data)
        if card.is_valid():
            card.save()
            return Response(status=201)
        else:
            return Response(status=424)
