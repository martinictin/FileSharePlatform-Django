from django import forms
import django_filters
from .models import Dokumenti, Korisnici, Student_Dokument


class FilterForm(django_filters.FilterSet):
    class Meta:
        model = Dokumenti
        fields = ('Kreator_id',)
        
        Kreator_id = forms.ModelChoiceField(queryset=Dokumenti.objects.all())
    
