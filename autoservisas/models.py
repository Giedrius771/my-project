from PIL import Image
from django.db import models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField

class AutomobilioModelis(models.Model):
    marke = models.CharField(max_length=255)
    modelis = models.CharField(max_length=255)
    description = HTMLField()

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilio modeliai'

class Automobilis(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('pending', 'Pending'),
    ]

    valstybinis_numeris = models.CharField(max_length=20)
    automobilio_modelis = models.ForeignKey(AutomobilioModelis, on_delete=models.CASCADE)
    vin_kodas = models.CharField(max_length=17)
    klientas = models.CharField(max_length=255)
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    due_back = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.valstybinis_numeris

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

    resized_cover = models.ImageField('Viršelis (Resized)', upload_to='resized_covers', null=True, blank=True)

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.cover:
        # Open the uploaded image using Pillow
        image = Image.open(self.cover.path)

        # Resize the image while preserving the aspect ratio
        target_size = (300, 300)
        image.thumbnail(target_size)

        # Save the resized image
        resized_image_path = self.cover.path.replace('covers', 'resized_covers')
        image.save(resized_image_path)

        # Update the 'resized_cover' field with the resized image path
        self.resized_cover = self.cover.name.replace('covers', 'resized_covers')
        self.save()

class Paslauga(models.Model):
    pavadinimas = models.CharField(max_length=255)

    def __str__(self):
        return self.pavadinimas

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Uzsakymas(models.Model):
    STATUS_CHOICES = (
        ('N', 'Naujas'),
        ('V', 'Vykdomas'),
        ('U', 'Užbaigtas'),
        ('A', 'Atšauktas'),
    )

    statusas = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    data = models.DateField(verbose_name='Data', null=True, blank=True)
    automobilis = models.ForeignKey(Automobilis, on_delete=models.CASCADE)
    suma = models.CharField(max_length=255)
    pavadinimas = models.CharField(max_length=255)
    kaina = models.IntegerField()

    def __str__(self):
        return f"{self.automobilis.klientas} - {self.automobilis.automobilio_modelis} - {self.data}"

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'


class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey(Paslauga, on_delete=models.CASCADE)
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE)
    kiekis = models.CharField(max_length=255)
    kaina = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'


class Password(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user