from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
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
import io
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from random import randint
import difflib


class ListCardsView(LoginRequiredMixin, ListView):
    model = Cards
    template_name = 'cards/cards.html'
    context_object_name = 'cards'
    paginate_by = 13
    ordering = ['-created_at']

    def get_queryset(self):
        ordering = self.get_ordering()
        queryset = self.model._default_manager.filter(
            deck=self.kwargs['pk']
        ).values('id', 'question', 'created_at', 'review_date').order_by(*ordering)
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck_id'] = self.kwargs['pk']
        context['title'] = Decks.objects.get(id=self.kwargs['pk'])
        return context


class AllCardsView(LoginRequiredMixin, ListView):
    model = Cards
    template_name = 'cards/cards.html'
    context_object_name = 'cards'
    paginate_by = 13
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все карточки'
        return context


class DetailCardView(LoginRequiredMixin, DetailView):
    context_object_name = 'card'
    model = Cards
    template_name = 'cards/show_card.html'


class CreateCardView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Cards
    form_class = CreateCardForm
    template_name = 'form.html'
    success_message = 'Карточка успешно добавлена'

    def get_success_url(self):
        return reverse_lazy('decks:cards', kwargs={'pk': self.kwargs['pk']})

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
            messages.error(
                self.request, 'Невозможно добавить карточку в несуществующую колоду')
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
        return context


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
        context['text_button'] = 'Удалить'
        return context


@login_required
def upload_file(request, pk):
    try:
        Decks.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(
            request, 'Невозможно добавить карточки в несуществующую колоду')
        return redirect('decks:decks')
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
                            random_num=randint(1, 2000)
                        )
                    messages.success(
                        request, 'Карточки были успешно импортированы')
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


@login_required
def download_file(request, pk=None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cards.csv"'
    writer = csv.writer(response)
    if pk:
        cards = Cards.objects.filter(deck=pk)
    else:
        cards = Cards.objects.filter(created_by=request.user.id)
    for card in cards:
        writer.writerow([card.question, card.answer])
    return response


def check_answer(request, card_id):
    try:
        Cards.objects.get(id=card_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Такой карточки нет')
        return redirect('/')
    else:
        if request.method == 'POST':
            quality = int(request.POST.get('quality'))
            if quality not in [1, 2, 3, 4, 5]:
                messages.error(request, 'Нет такой категории ответа')
                return redirect('/')
            else:
                card = Cards.objects.get(id=card_id)
                if card.review_date:
                    # изменил код в SMTwo: была ошибка, из-за того что карточки не повторялись в заданный день
                    # добавил условие, что если дата повторения карточки не равна сегодняшней дате, то она изменяется
                    # на сегодняшнюю
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
    template_name = 'cards/cards_learn.html'
    context_object_name = 'card'
    model = Cards

    def get_queryset(self):
        queryset = self.model._default_manager.filter(
            Q(review_date__isnull=True) | Q(review_date__lte=date.today())
        ).filter(
            deck=self.kwargs['pk']).values('id', 'question', 'question_type', 'style')
        if queryset:
            return queryset[0]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Cards.objects.filter(deck=self.kwargs['pk']).values('id')
        queryset = queryset.filter(
            Q(review_date__isnull=True) | Q(review_date__lte=date.today()))
        count = queryset.aggregate(count=Count('id'))
        context['count'] = count
        return context


def show_answer(request, card_id):
    try:
        card = Cards.objects.filter(id=card_id).values(
            'id', 'question', 'question_type', 'answer', 'answer_type', 'deck')[0]
    except ObjectDoesNotExist:
        messages.error(request, 'Такой карточки нет')
        return redirect('/')
    else:
        # если ответ нужно было ввести вручную
        if request.POST.get('answer'):
            pattern = card['answer']
            entered_word = request.POST.get('answer')
            diff = difflib.ndiff(pattern, entered_word)
            equals_answers = []
            for i in diff:
                if i[0] == '+':
                    equals_answers.append((i[-1], 'text-secondary'))
                if i[0] == '-':
                    equals_answers.append((i[-1], 'text-danger'))
                if i[0] == ' ':
                    equals_answers.append((i[-1], 'text-success'))
            return render(
                request,
                'cards/cards_answer.html',
                context={
                    'card': card,
                    'answer': entered_word,
                    'equals_answers': equals_answers
                }
            )
        else:
            return render(
                request,
                'cards/cards_answer.html',
                context={
                    'card': card,
                }
            )


def delete_select_cards(request, pk=None):
    selected = request.POST.getlist('select')
    if selected:
        for select_id in selected:
            card = Cards.objects.get(id=select_id)
            card.delete()
        messages.success(request, 'Карточки были успешно удалены')
    else:
        messages.error(request, 'Вы не выбрали ни одной карточки')
    if pk:
        return redirect(reverse_lazy('decks:cards', kwargs={'pk': pk}))
    else:
        return redirect(reverse_lazy('cards:all_cards'))


class DeleteAllCardsView(SuccessMessageMixin, DeleteView):
    template_name = 'delete.html'
    model = Cards
    success_url = reverse_lazy('decks:decks')
    success_message = 'Карточки успешно удалены'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk:
            deck = Decks.objects.get(id=pk)
            queryset = self.model._default_manager.filter(deck=deck)
        else:
            queryset = self.model._default_manager.filter(
                created_by=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.info(self.request, 'Колода пустая')
            return redirect('decks:decks')
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Удалить'
        if self.kwargs.get('pk'):
            context['deck'] = Decks.objects.get(id=self.kwargs['pk'])
        return context
