from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm
from main.models import Notice

from django.shortcuts import render, redirect


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



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    notices = Notice.objects.all()
    return render(request, 'main/profile.html', {
        'notices': notices,
        'car_brands': CAR_BRANDS,
        'car_models': CAR_MODELS,
        'region_choices': [r for r, _ in REGION_CHOICES],
    })
