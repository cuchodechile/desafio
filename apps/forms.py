from django.forms import forms
from django import forms
import  datetime

class ContactoForm(forms.Form):
    CHOICES=[('US','Dolar'),('UF','UF')]
   
  
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 20, cur_year + 1)])
    
    Indicador = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    inicio=forms.DateField(initial=datetime.date.today() - datetime.timedelta(days=7),widget=forms.SelectDateWidget(years=year_range))
    #inicio=forms.DateField(widget = forms.DateInput(format='%m-%Y'))
    final=forms.DateField(initial=datetime.date.today() - datetime.timedelta(days=7),widget=forms.SelectDateWidget(years=year_range))
    
 