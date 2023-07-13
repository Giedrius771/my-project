from django.contrib import admin
from django.utils import timezone
from .models import AutomobilioModelis, Automobilis, Paslauga, Uzsakymas, UzsakymoEilute

class UzsakymoEiluteInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 1

class UzsakymasAdmin(admin.ModelAdmin):
    inlines = (UzsakymoEiluteInline,)
    list_display = ('__str__', 'automobilis', 'data', 'suma', 'pavadinimas', 'kaina')

    def save_model(self, request, obj, form, change):
        obj.data = timezone.now().date()
        super().save_model(request, obj, form, change)

class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_numeris', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis')
    search_fields = ('valstybinis_numeris', 'vin_kodas')

admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Paslauga)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)