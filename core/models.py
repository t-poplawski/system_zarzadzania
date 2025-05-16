from django.db import models

# Create your models here
class Przedmiot(models.Model):
    czy_do_wyboru = models.BooleanField()
    nazwa = models.CharField(max_length=200, unique=True)
    sem = models.IntegerField()
    ects = models.IntegerField()
    instytut = models.CharField(max_length=50)
    katedra = models.CharField(max_length=50)
    
    POZIOM_CHOICES = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('JM', 'JM'),
    ]
    poziom = models.CharField(
        max_length=3, # najdłuższe jest 'III'
        choices=POZIOM_CHOICES,
    )
    
    specjalizacja = models.CharField(max_length=50, blank=True, null=True) # zakładam że może być puste
    lokalizacja = models.CharField(max_length=50)
    jezyk = models.CharField(max_length=20)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = "Przedmiot"
        verbose_name_plural = "Przedmioty"

class Grupa(models.Model):
    grupa = models.CharField(max_length=20, unique=True)
    kierunek = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.kierunek} - {self.grupa}"

    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "Grupy"
        constraints = [
            models.UniqueConstraint(
                fields=['grupa', 'kierunek'],
                name='unikalna_grupa_na_kierunku'
            )
        ] # nie może być dwóch tych samych grup na jednym kierunku

class Pracownik(models.Model):
    imie_nazwisko = models.CharField(max_length=100)
    stanowisko = models.CharField(max_length=50)
    instytut = models.CharField(max_length=50) 
    katedra = models.CharField(max_length=50)  

    def __str__(self):
        return self.imie_nazwisko

    class Meta:
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"

class RokAkademicki(models.Model):
    rok = models.CharField(
        max_length=9,
        unique=True,
        help_text="Format RRRR/RRRR"
    )

    def __str__(self):
        return self.rok

    class Meta:
        verbose_name = "Rok akademicki"
        verbose_name_plural = "Lata akademickie"

class PrzedmiotRok(models.Model):
    przedmiot = models.ForeignKey(
        'Przedmiot',
        on_delete=models.CASCADE,
    )
    rok_akademicki = models.ForeignKey(
        'RokAkademicki',
        on_delete=models.CASCADE,
    )
    grupa = models.ForeignKey(
        'Grupa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    forma_zaliczenia = models.CharField(max_length=20, null=True, blank=True)
    liczba_godz = models.IntegerField()

    FORMA_ZAJEC_CHOICES = [
        ('ĆW', 'ĆW'),
        ('LB', 'LB'),
        ('W', 'W'),
        ('K', 'K'),
        ('S', 'S'),
    ]
    forma_zajec = models.CharField(
        max_length=2, # najdłuższy klucz to 2 znaki (ĆW, LB)
        choices=FORMA_ZAJEC_CHOICES,
    )

    prowadzacy = models.ForeignKey(
        'Pracownik',
        on_delete=models.CASCADE,
        related_name='prowadzone_przedmioty', # nazwa dla relacji
    )
    koordynator_sylabusa = models.ForeignKey(
        'Pracownik',
        on_delete=models.CASCADE,
        related_name='koordynowane_sylabusy',
    )

    RODZAJ_CHOICES = [
        ('S', 'S'),
        ('NZ', 'NZ'),
    ]
    rodzaj = models.CharField(
        max_length=2,
        choices=RODZAJ_CHOICES,
    )

    rok_ob = models.IntegerField(blank=True, null=True)
    ilosc_st_na_sem = models.IntegerField(blank=True, null=True)
    liczba_godz_obc = models.IntegerField() # w excel nie ma pustych pól, jedynie 0

    uwagi = models.TextField(blank=True, null=True)
    czy_przed_wyborem = models.BooleanField(null=True, blank=True)

    def __str__(self):
        przedmiot_nazwa = self.przedmiot.nazwa if self.przedmiot else "Brak przedmiotu"
        rok_nazwa = self.rok_akademicki.rok if self.rok_akademicki else "Brak roku"
        forma_zajec_display = self.get_forma_zajec_display() if self.forma_zajec else "Brak formy zajęć"
        return f"{przedmiot_nazwa} ({forma_zajec_display}) - {rok_nazwa}"

    class Meta:
        verbose_name = "Realizacja przedmiotu w roku"
        verbose_name_plural = "Realizacje przedmiotów w latach"

class PracownikRok(models.Model):
    pracownik = models.ForeignKey(
        'Pracownik',
        on_delete=models.CASCADE,
        related_name='roczne_dane'
    )
    rok_akademicki = models.ForeignKey(
        'RokAkademicki',
        on_delete=models.CASCADE,
        related_name='dane_pracownikow_w_roku'
    )
    pensum_stanowisko = models.FloatField()
    pensum_pracownika = models.FloatField()
    inne_godz = models.FloatField(null=True, blank=True)
    obciazenie = models.FloatField()

    def __str__(self):
        pracownik_str = str(self.pracownik) if self.pracownik else "Brak pracownika"
        rok_str = str(self.rok_akademicki) if self.rok_akademicki else "Brak roku"
        return f"{pracownik_str} - {rok_str}"

    class Meta:
        verbose_name = "Dane roczne pracownika"
        verbose_name_plural = "Dane roczne pracowników"
        constraints = [
            models.UniqueConstraint(
                fields=['pracownik', 'rok_akademicki'],
                name='unikalne_dane_pracownika_na_rok'
            )
        ] # na jeden rok akademicki może być jeden pracownik