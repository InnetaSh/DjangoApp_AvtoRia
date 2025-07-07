from django import forms
from .models import Notice

class AvtoRiaForm(forms.ModelForm):
    year = forms.IntegerField(min_value=1985, max_value=2025, label="Год выпуска")
    price = forms.IntegerField(min_value=500, max_value=500000, label="Цена($)")

    class Meta:
        model = Notice
        fields = ['title','region', 'marka', 'model', 'year', 'price', 'mileage', 'description', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_class + ' inputBlock').strip()
