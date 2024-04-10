from django.forms import model_to_dict
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from app.forms import LoginForm, RegistrationForm, SettingsForm, NewQuestionForm, NewAnswerForm
from . import models
from app.models import Question, Answer, Tag, Profile, Like


def index(request):
    question_list = models.Question.objects.top()
    popular_tags = models.Tag.objects.popular_tags()
    best_users = models.Profile.objects.top_profiles()
    page_obj = paginate(question_list, request, 20)

    context = {
        'page_obj': page_obj,
        'popular_tags': popular_tags,
        'best_users': best_users,
    }

    return render(request, 'index.html', context=context)

@require_http_methods(['GET','POST'])
def question(request, question_id: int):
    if question_id > models.Question.objects.count():
        return render(request, '404.html')
    else:
        popular_tags = models.Tag.objects.popular_tags()
        best_users = models.Profile.objects.top_profiles()
        print(question_id)
        print(models.Question.objects.count())
        print( models.Question.objects)
        question_item = models.Question.objects.get(id = question_id)
        answers = models.Answer.objects.ordered_answers(question_id)
        if request.method == 'GET':
            form = NewAnswerForm(request.user, question_item)
        if request.method == 'POST':
            form = NewAnswerForm(request.user, request.POST)
            if form.is_valid():
                answer = form.save()
                if answer:  
                    answer.user = request.user
                    answer.question = question_item.id
                    answer.save()
                    zero_like = models.Like.objects.create(content_type = ContentType.objects.get_for_model(Answer), value = 0, owner = request.user, object_id = answer.id)
                    return redirect(reverse('question') + question_id)
                else:
                    form.add_error(field=None,error="Something wrong!")
            
        context = {
            'form' : form,
            'popular_tags': popular_tags,
            'best_users': best_users,
            'question': question_item,
            'answers': answers,
            }
        return render(request,'question.html',context=context)


@require_http_methods(['GET','POST'])
def log_in(request):
    popular_tags = models.Tag.objects.popular_tags()
    best_users = models.Profile.objects.top_profiles()
    context = {
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    if request.method == 'GET':
        user_form = LoginForm()
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            
            if user:
                auth.login(request=request, user=user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None,error="Wrong username or password!")
    context = {
        'form': user_form,
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    return render(request,'log_in.html',context=context)


@require_http_methods(['GET','POST'])
def register(request):
    popular_tags = models.Tag.objects.popular_tags()
    best_users = models.Profile.objects.top_profiles()
    context = {
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    if request.method == 'GET':
        user_form = RegistrationForm()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:   
                profile = models.Profile.objects.create(owner=user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None,error="Something wrong!")
    context = {
        'form': user_form,
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    return render(request,'register.html',context=context)


@login_required(login_url='log_in', redirect_field_name='continue')
def new_question(request):
    popular_tags = models.Tag.objects.popular_tags()
    best_users = models.Profile.objects.top_profiles()
    if request.method == 'GET':
        form = NewQuestionForm(request.user)
    if request.method == 'POST':
        form = NewQuestionForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            if question:  
                zero_like = models.Like.objects.create(content_type = ContentType.objects.get_for_model(Question), value = 0, owner = request.user.profile, object_id = question.id)
                return redirect('question', question_id=question.id)
            else:
                form.add_error(field=None,error="Something wrong!")
    context = {
        'form': form,
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    return render(request, 'new_question.html',context=context)


def questions_by_tag(request, tag_id: int):
    tag = models.Tag.objects.get(id = tag_id)
    question_list = models.Question.objects.tag(tag_id)
    popular_tags = models.Tag.objects.popular_tags()
    best_users = models.Profile.objects.top_profiles()
    page_obj = paginate(question_list, request, 20)

    context = {
        'tag' : tag,
        'page_obj': page_obj,
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    return render(request, 'questions_by_tag.html', context=context)


@login_required(login_url='log_in', redirect_field_name='continue')
@require_http_methods(['GET','POST'])
def settings(request):
    popular_tags = models.Tag.objects.popular_tags()
    best_users = models.Profile.objects.top_profiles()
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        form = SettingsForm(initial=initial_data)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect(reverse('settings'))
    context = {
        'form': form,
        'popular_tags': popular_tags,
        'best_users': best_users,
    }
    return render(request, 'settings.html',context=context)


def log_out(request):
    auth.logout(request)
    return redirect(reverse('index'))


def paginate(objects_list, request, items_per_page=20):
    paginator = Paginator(objects_list, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj