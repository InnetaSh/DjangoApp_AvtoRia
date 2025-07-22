from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    CAR_BRANDS = [
        ('Toyota', 'Toyota'),
        ('BMW', 'BMW'),
        ('Audi', 'Audi'),
        ('Mercedes', 'Mercedes'),
    ]

    REGION_CHOICES = [(r, r) for r in [
        'Винницкая', 'Волынская', 'Днепропетровская', 'Донецкая', 'Житомирская',
        'Закарпатская', 'Запорожская', 'Ивано-Франковская', 'Киевская', 'Кировоградская',
        'Луганская', 'Львовская', 'Николаевская', 'Одесская', 'Полтавская', 'Ровненская',
        'Сумская', 'Тернопольская', 'Харьковская', 'Херсонская', 'Хмельницкая',
        'Черкасская', 'Черниговская', 'Черновицкая', 'г. Киев', 'г. Севастополь', 'АР Крым'
    ]]

    title = models.CharField("Название объявления", max_length=250)
    region = models.CharField("Регион", choices=REGION_CHOICES, max_length=100)
    marka = models.CharField("Марка", choices=CAR_BRANDS, max_length=100)
    model = models.CharField("Модель", max_length=100)
    year = models.PositiveIntegerField("Год выпуска")
    price = models.DecimalField("Цена ($)", max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField("Пробег (км)")
    description = models.TextField("Описание")
    photo = models.ImageField("Фото", upload_to="cars/", blank=True, null=True)
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')

    def __str__(self):
        return f"{self.marka} {self.model} ({self.year})"



class ViewedNotice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_notices')
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField("Дата просмотра", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} viewed {self.notice} at {self.viewed_at}"


class FavoriteNotice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_notices')
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    added_at = models.DateTimeField("Дата добавления в избранное", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} added {self.notice} to favorites"

