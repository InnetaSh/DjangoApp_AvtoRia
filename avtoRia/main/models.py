from django.db import models

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

    def __str__(self):
        return f"{self.marka} {self.model} ({self.year})"
