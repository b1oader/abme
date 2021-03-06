from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from film.models import FilmRating, FilmWatchlist
from serial.models import SerialRating, SerialWatchlist
from api.models import Serial, Film, Article
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from search.views import Round
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, UserForm


def signup(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully, login.')
            return redirect('website_login')

    else:
        f = CustomUserCreationForm()

    return render(request, 'user/signup.html', {'form': f})


@login_required
@transaction.atomic
def settings(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated! '))
            return redirect('user_settings')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    activ_user = get_object_or_404(User, username=request.user)
    activ_profile = get_object_or_404(Profile, user=activ_user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'activ_profile': activ_profile,
    }

    return render(request, 'user/settings.html', context)


@login_required
@transaction.atomic
def settings_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, ('Your password was successfully updated! '))
            return redirect('user_settings_password')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        'password_form': password_form,
    }

    return render(request, 'user/settings_password.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    var = get_object_or_404(Profile, user=user)
    full_name = user.first_name + " " + user.last_name

    filmrating = FilmRating.objects.filter(user=user)
    serialrating = SerialRating.objects.filter(user=user)

    f_ratings = filmrating.order_by('-rate')[0:4]
    s_ratings = serialrating.order_by('-rate')[0:4]

    user_votes = []
    for i in range(1, 11):
        fvotes = filmrating.filter(rate=i).count()
        svotes = serialrating.filter(rate=i).count()
        user_votes.append(fvotes + svotes)

    all_votes = sum(user_votes)
    max_vote = max(user_votes)

    f_rating_count = filmrating.count()
    s_rating_count = serialrating.count()

    context = {
        'user': user,
        'full_name': full_name,
        'f_ratings': f_ratings,
        's_ratings': s_ratings,
        'all_votes': all_votes,
        'user_votes': user_votes,
        'max_vote': max_vote,
        'user_films_count': f_rating_count,
        'user_serials_count': s_rating_count,
    }
    return render(request, 'user/profile.html', context)


def profile_films(request, username):
    user = get_object_or_404(User, username=username)
    var = get_object_or_404(Profile, user=user)

    page = request.GET.get('page')
    order_by = request.GET.get('order_by', '-date')

    f_ratings = FilmRating.objects.filter(user=user).order_by(order_by)

    paginator = Paginator(f_ratings, per_page=10)
    try:
        f_ratings = paginator.page(page)
    except PageNotAnInteger:
        f_ratings = paginator.page(1)
    except EmptyPage:
        f_ratings = paginator(paginator.num_pages)

    context = {
        'user': user,
        'f_ratings': f_ratings,
    }
    return render(request, 'user/profile_films.html', context)


def profile_serials(request, username):
    user = get_object_or_404(User, username=username)
    var = get_object_or_404(Profile, user=user)

    page = request.GET.get('page')
    order_by = request.GET.get('order_by', '-date')

    s_ratings = SerialRating.objects.filter(user=user).order_by(order_by)

    paginator = Paginator(s_ratings, per_page=10)
    try:
        s_ratings = paginator.page(page)
    except PageNotAnInteger:
        s_ratings = paginator.page(1)
    except EmptyPage:
        s_ratings = paginator(paginator.num_pages)

    context = {
        'user': user,
        's_ratings': s_ratings,
    }
    return render(request, 'user/profile_serials.html', context)


@login_required
def watchlist(request):
    del_film_watchlist = request.GET.get('del_film_watchlist', None)
    del_serial_watchlist = request.GET.get('del_serial_watchlist', None)

    activ_user = get_object_or_404(User, username=request.user)

    if request.method == 'GET':
        if del_film_watchlist is not None:
            film = get_object_or_404(Film, id=del_film_watchlist)
            FilmWatchlist.objects.filter(user=activ_user, film=film).delete()

        if del_serial_watchlist is not None:
            serial = get_object_or_404(Serial, id=del_serial_watchlist)
            SerialWatchlist.objects.filter(user=activ_user, serial=serial).delete()

    watchlist_f = FilmWatchlist.objects.filter(user=activ_user).annotate(
        average_score=Coalesce(Round(Avg('film__filmrating__rate')), 0),
        votes=Count('film__filmrating__user', distinct=True))

    watchlist_s = SerialWatchlist.objects.filter(user=activ_user).annotate(
        average_score=Coalesce(Round(Avg('serial__serialrating__rate')), 0),
        votes=Count('serial__serialrating__user', distinct=True))

    latest_article = Article.objects.get_queryset().order_by('-created_date').first()

    page = request.GET.get('page')
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order')

    watchlist_all = sorted(
        chain(watchlist_f, watchlist_s),
        key=attrgetter('id'))

    if sort_by == "Global rating":
        if order == 'Ascending':
            watchlist_all = sorted(
                chain(watchlist_f, watchlist_s),
                key=attrgetter('average_score'),
                reverse=False)
        if order == 'Descending':
            watchlist_all = sorted(
                chain(watchlist_f, watchlist_s),
                key=attrgetter('average_score'),
                reverse=True)
    if sort_by == "Data added":
        if order == 'Ascending':
            watchlist_all = sorted(
                chain(watchlist_f, watchlist_s),
                key=attrgetter('date'),
                reverse=False)
        if order == 'Descending':
            watchlist_all = sorted(
                chain(watchlist_f, watchlist_s),
                key=attrgetter('date'),
                reverse=True)
    if sort_by == "Popularity":
        if order == 'Ascending':
            watchlist_all = sorted(
                chain(watchlist_f, watchlist_s),
                key=attrgetter('votes'),
                reverse=False)
        if order == 'Descending':
            watchlist_all = sorted(
                chain(watchlist_f, watchlist_s),
                key=attrgetter('votes'),
                reverse=True)

    paginator = Paginator(watchlist_all, per_page=12)
    try:
        watchlist_all = paginator.page(page)
    except PageNotAnInteger:
        watchlist_all = paginator.page(1)
    except EmptyPage:
        watchlist_all = paginator(paginator.num_pages)

    context = {
        'watchlist_all': watchlist_all,
        'latest_article': latest_article,
    }
    return render(request, 'user/watchlist.html', context)
