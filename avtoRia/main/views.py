import json
import os.path
from datetime import datetime, timezone
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import decimal

from .form import AvtoRiaForm
from users.form import UserRegisterForm
from django.core.files.storage import FileSystemStorage
import json.decoder


from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from .models import Notice, ViewedNotice, FavoriteNotice
from django.contrib.auth.decorators import login_required




CAR_MODELS = {
    'Toyota': ['Camry', 'Corolla', 'Prado'],
    'BMW': ['X5', 'X6', 'M3'],
    'Audi': ['A4', 'Q7', 'A6'],
    'Mercedes': ['C-Class', 'E-Class', 'S-Class'],
}

CAR_BRANDS = list(CAR_MODELS.keys())

REGION_CHOICES = [(r, r) for r in [
    'Винницкая', 'Волынская', 'Днепропетровская', 'Донецкая', 'Житомирская',
    'Закарпатская', 'Запорожская', 'Ивано-Франковская', 'Киевская', 'Кировоградская',
    'Луганская', 'Львовская', 'Николаевская', 'Одесская', 'Полтавская', 'Ровненская',
    'Сумская', 'Тернопольская', 'Харьковская', 'Херсонская', 'Хмельницкая',
    'Черкасская', 'Черниговская', 'Черновицкая', 'г. Киев', 'г. Севастополь', 'АР Крым'
]]




def home_view(request):
    notices = Notice.objects.all()
    return render(request, 'main/home.html', {
        'notices': notices,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })


def filter_result(request):
    marka = request.GET.get('marka', '')
    model = request.GET.get('model', '')
    region = request.GET.get('region', '')

    notices = Notice.objects.all()
    if marka:
        notices = notices.filter(marka=marka)
    if model:
        notices = notices.filter(model=model)
    if region:
        notices = notices.filter(region=region)

    return render(request, 'main/home.html', {
        'notices': notices,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })


def add_notice_view(request):
    if request.method == 'POST':
        form = AvtoRiaForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.timestamp = datetime.now()
            notice.save()

            return redirect('all_notice')
    else:
        form = AvtoRiaForm()

    return render(request, 'main/create_ad.html', {
        'form': form,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
    })

def detail(request, notice_id):
    note = get_object_or_404(Notice, id = notice_id)
    ViewedNotice.objects.create(
        user=request.user,
        notice=note,
        viewed_at=timezone.now()
    )

    return render(request, 'main/detail.html', {
        'notice': note
    })


@login_required
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id, user=request.user)
    notice.delete()
    notices = Notice.objects.all()
    favorite_ids = request.user.favorite_notices.values_list('notice_id', flat=True)
    return render(request, 'main/profile.html', {
        'notices': notices,
        'favorite_ids': list(favorite_ids),
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })



@login_required
def all_notice(request):
    notices = Notice.objects.all()
    favorite_ids = request.user.favorite_notices.values_list('notice_id', flat=True)
    return render(request, 'main/profile.html', {
        'notices': notices,
        'favorite_ids': list(favorite_ids),
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })

@login_required
def my_notice(request):
    notices = Notice.objects.filter(user=request.user)
    favorite_ids = request.user.favorite_notices.values_list('notice_id', flat=True)
    return render(request, 'main/profile.html', {
        'notices': notices,
        'favorite_ids': list(favorite_ids),
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })

@login_required
def notice_24hour(request):
    time_threshold = now() - timedelta(hours=24)
    viewed_notices = ViewedNotice.objects.filter(user=request.user, viewed_at__gte=time_threshold).values_list('notice_id', flat=True)
    notices = Notice.objects.filter(id__in=viewed_notices)
    favorite_ids = request.user.favorite_notices.values_list('notice_id', flat=True)
    return render(request, 'main/profile.html', {
        'notices': notices,
        'favorite_ids': list(favorite_ids),
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })

@login_required
def favorite_notice(request):
    favorites = FavoriteNotice.objects.filter(user=request.user).values_list('notice_id', flat=True)
    notices = Notice.objects.filter(id__in=favorites)
    favorite_ids = request.user.favorite_notices.values_list('notice_id', flat=True)
    return render(request, 'main/profile.html', {
        'notices': notices,
        'favorite_ids': list(favorite_ids),
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })



@login_required
def add_to_favorites(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    FavoriteNotice.objects.get_or_create(user=request.user, notice=notice)
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

@login_required
def remove_from_favorites(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    FavoriteNotice.objects.filter(user=request.user, notice=notice).delete()
    return redirect(request.META.get('HTTP_REFERER', 'profile'))


def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id, user=request.user)  # Только свои объявления

    if request.method == 'POST':
        form = AvtoRiaForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('my_notice')
    else:
        form = AvtoRiaForm(instance=notice)

    return render(request, 'main/edit_notice.html', {
        'form': form,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
        'notice': notice,
    })







def home_view2(request):
    json_path = os.path.join(settings.BASE_DIR, 'data', 'message.json')
    notices = []

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            notices = json.load(file)

    return render(request, 'main/home.html', {'notices': notices,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })


def filter_result2(request):
    marka = request.GET.get('marka', '')
    model = request.GET.get('model', '')
    region = request.GET.get('region', '')

    json_path = os.path.join(settings.BASE_DIR, 'data', 'message.json')
    notices = []

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for notice in data:
                if (
                    (not marka or notice.get('marka') == marka) and
                    (not model or notice.get('model') == model) and
                    (not region or notice.get('region') == region)
                ):
                    notices.append(notice)

    return render(request, 'main/home.html', {
        'notices': notices,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })


def add_notice_view2(request):
    if request.method == 'POST':
        form = AvtoRiaForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.timestamp = datetime.now()
            notice.save()
            return redirect('home')
    else:
        form = AvtoRiaForm()

    return render(request, 'main/create_ad.html', {
        'form': form,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
    })




def add_notice_view2(request):
    if request.method == 'POST':
        form = AvtoRiaForm(request.POST, request.FILES)
        if form.is_valid():
            message_data = form.cleaned_data.copy()
            message_data["timestamp"] = datetime.now().isoformat()

            photo = form.cleaned_data.get('photo')
            if photo:
                fs = FileSystemStorage()
                filename = fs.save(photo.name, photo)
                uploaded_file_url = fs.url(filename)
                message_data['photo'] = filename
            else:
                message_data['photo'] = ''

            for key, value in message_data.items():
                if isinstance(value, decimal.Decimal):
                    message_data[key] = float(value)

            json_path = os.path.join(settings.BASE_DIR, 'data', 'message.json')
            os.makedirs(os.path.dirname(json_path), exist_ok=True)

            data = []
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        if content:
                            data = json.loads(content)
                        else:
                            data = []
                except (json.decoder.JSONDecodeError, ValueError):
                    data = []

            data.append(message_data)

            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return redirect('home')
    else:
        form = AvtoRiaForm()

    return render(request, 'main/create_ad.html', {
        'form': form,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
    })


def filter_form(request):
    return render(request, 'main/filter.html', {
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })



