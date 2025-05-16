from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Przedmiot)
admin.site.register(Grupa)
admin.site.register(Pracownik)
admin.site.register(RokAkademicki)
admin.site.register(PrzedmiotRok)
admin.site.register(PracownikRok)