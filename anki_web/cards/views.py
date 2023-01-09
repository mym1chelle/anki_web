from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView,\
    ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from datetime import date
from supermemo2 import SMTwo
import csv
from anki_web.styles.models import Styles
from .models import Cards
from anki_web.users.models import Users
from anki_web.decks.models import Decks
from .forms import CreateCardForm, UploadFileForm
from django.contrib import messages
from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.core.exceptions import ImproperlyConfigured
import io
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from random import randint
# импорт для DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CardsListSerializer, DetailCardSerializer, CreateCardSerializer


class ListCardsView(LoginRequiredMixin, ListView):
    model = Cards
    template_name = 'cards/cards.html'
    context_object_name = 'cards'
    paginate_by = 13

    def get_queryset(self):

        if self.model is not None:
            queryset = self.model._default_manager.filter(deck=self.kwargs['pk'])
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck_id'] = self.kwargs['pk']
        return context


class DetailCardView(LoginRequiredMixin, DetailView):
    context_object_name = 'card'
    model = Cards
    template_name = 'cards/show_card.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        hidden = request.GET.get('showFullText')
        if hidden:
            context['showFullText'] = True
        return self.render_to_response(context)


class CreateCardView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Cards
    form_class = CreateCardForm
    template_name = 'form.html'
    success_message = 'Карточка успешно добавлена'

    def get_success_url(self):
        url = reverse_lazy('decks:cards', kwargs={'pk': self.kwargs['pk']})
        return url

    def get(self, request, *args, **kwargs):
        try:
            Decks.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'Такой колоды не существует')
            return redirect('decks:decks')
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            Decks.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'Невозможно добавить карточку в несуществующую колоду')
            return redirect('decks:decks')
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = Users.objects.get(pk=self.request.user.id)
        form.instance.deck = Decks.objects.get(pk=self.kwargs['pk'])
        form.instance.random_num = randint(1, 2000)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Создать'


class UpdateCardView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = Cards
    form_class = CreateCardForm
    template_name = 'form.html'
    success_url = reverse_lazy('main_page')
    success_message = 'Карточка успешно обновлена'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Обновить'
        return context


class DeleteCardView(SuccessMessageMixin, DeleteView):
    template_name = 'delete.html'
    model = Cards
    success_url = reverse_lazy('decks:decks')
    success_message = 'Карточка успешно удалена'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button '] = 'Удалить'
        return context


@login_required
def upload_file(request, pk):
    try:
        Decks.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Невозможно добавить карточки в несуществующую колоду')
        return redirect('/')
    else:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                question_type = request.POST['question_type']
                answer_type = request.POST['answer_type']
                style = request.POST['card_style']
                with io.TextIOWrapper(file, encoding="utf-8", newline='\n') as text_file:
                    read = csv.reader(text_file)
                    deck = Decks.objects.get(pk=pk)
                    style = Styles.objects.get(pk=int(style))
                    user = Users.objects.get(pk=request.user.id)
                    for row in read:
                        question = row[0]
                        answer = row[1]
                        Cards.objects.create(
                            question=question,
                            question_type=question_type,
                            answer=answer,
                            answer_type=answer_type,
                            style=style,
                            deck=deck,
                            created_by=user,
                            random_num = randint(1, 2000)
                        )
                    messages.success(request, 'Карточки были успешно импортированы')
                return redirect(reverse_lazy('decks:cards', kwargs={'pk': pk}))
        else:
            form = UploadFileForm()
        return render(
            request,
            'cards/upload.html',
            context={
                'form': form,
                'text_button': 'Импортировать'
            }
        )


def check_answer(request, quality, card_id):
    try:
        Cards.objects.get(id=card_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Такой карточки нет')
        return redirect('/')
    else:
        if quality not in [1, 2, 3, 4, 5]:
            messages.error(request, 'Нет такой категории ответа')
            return redirect('/')
        else:
            if request.method == 'POST':
                card = Cards.objects.get(id=card_id)
                if card.review_date:
                    review = SMTwo(
                        card.easiness,
                        card.interval,
                        card.repetitions
                    ).review(quality, card.review_date)
                else:
                    review = SMTwo.first_review(quality=quality)
                card.easiness = review.easiness
                card.interval = review.interval
                card.repetitions = review.repetitions
                card.review_date = review.review_date
                card.save()
                id = card.deck.id
                return redirect(f'/decks/{id}/learn/')


class ListCardsDayView(LoginRequiredMixin,
                       ListView):
    paginate_by = 1
    template_name = 'cards/cards_learn.html'
    context_object_name = 'cards'
    model = Cards

    def get_queryset(self):

        if self.model is not None:
            queryset = self.model._default_manager.filter(deck=self.kwargs['pk'])
            queryset = queryset.filter(Q(review_date__isnull=True) | Q(review_date__lte=date.today()))
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Cards.objects.filter(deck=self.kwargs['pk'])
        queryset = queryset.filter(Q(review_date__isnull=True) | Q(review_date__lte=date.today()))
        count = queryset.aggregate(count=Count('question'))
        context['count'] = count
        return context


def show_answer(request, card_id):
    try:
        Cards.objects.get(id=card_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Такой карточки нет')
        return redirect('/')
    else:
        card = Cards.objects.get(id=card_id)
        deck = Decks.objects.get(id=card.deck.id)
        queryset = Cards.objects.filter(deck=deck)
        queryset = queryset.filter(Q(review_date__isnull=True) | Q(review_date__lte=date.today()))
        count = queryset.aggregate(count=Count('question'))
        if request.POST.get('answer'):
            return render(
                request,
                'cards/cards_answer.html',
                context={
                    'card': card,
                    'count': count,
                    'answer': request.POST.get('answer')
                }
            )
        else:
            return render(
                request,
                'cards/cards_answer.html',
                context={
                    'card': card,
                    'count': count
                }
            )


def delete_select_cards(request, pk):
    selected = request.POST.getlist('select')
    if selected:
        for select_id in selected:
            card = Cards.objects.get(id=select_id)
            card.delete()
        messages.success(request, 'Карточки были успешно удалены')
    else:
        messages.error(request, 'Вы не выбрали ни одной карточки')
    return redirect(reverse_lazy('decks:cards', kwargs={'pk': pk}))


def delete_all_cards(request, pk):
    deck = Decks.objects.get(id=pk)
    cards = Cards.objects.filter(deck=deck)
    for card in cards:
        card.delete()
    messages.success(request, 'Карточки были успешно удалены')
    return redirect(reverse_lazy('decks:cards', kwargs={'pk': pk}))


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
