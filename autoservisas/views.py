from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Automobilis, Uzsakymas, Paslauga
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from .models import Password
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView


def index(request):
    num_autoservisai = Automobilis.objects.all().count()
    num_uzsakymai = Uzsakymas.objects.all().count()
    num_instances_available = Uzsakymas.objects.filter(statusas__exact='Available').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_autoservisai': num_autoservisai,
        'num_uzsakymai': num_uzsakymai,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def statistics(request):
    paslaugu_kiekis = Paslauga.objects.count()
    uzsakymu_kiekis = Uzsakymas.objects.count()
    automobiliu_kiekis = Automobilis.objects.count()

    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'uzsakymu_kiekis': uzsakymu_kiekis,
        'automobiliu_kiekis': automobiliu_kiekis
    }

    return render(request, 'statistics.html', context)

def automobiliai(request):
    automobiliai = Automobilis.objects.all()
    paginator = Paginator(automobiliai, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'automobiliai.html', {'page_obj': page_obj})

class UzsakymaiListView(ListView):
    model = Uzsakymas
    template_name = 'uzsakymai.html'
    context_object_name = 'uzsakymai'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().order_by('id')

class UzsakymasDetailView(DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    context_object_name = 'uzsakymas'

def automobilis_detail(request, pk):
    automobilis = get_object_or_404(Automobilis, pk=pk)
    return render(request, 'automobilis_detail.html', {'automobilis': automobilis})

class AutomobilisDetailView(DetailView):
    model = Automobilis
    template_name = 'automobilis_detail.html'
    context_object_name = 'automobilis'


def search(request):
    query = request.GET.get('query')
    automobiliai = Automobilis.objects.filter(automobilio_modelis__marke__icontains=query)
    return render(request, 'search.html', {'automobiliai': automobiliai, 'query': query})


class LoanedAutomobiliaiByUserListView(LoginRequiredMixin, generic.ListView):
    model = Automobilis
    template_name = 'user_automobiliai.html'
    paginate_by = 10

    def get_queryset(self):
        return Automobilis.objects.filter(reader=self.request.user)


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # Generate the password reset link
        reset_url = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', args=[form.cleaned_data['uid'], form.cleaned_data['token']])
        )

        # Print the password reset link to the terminal
        print(f'Password reset link: {reset_url}')

        # Return a success response
        return super().form_valid(form)

