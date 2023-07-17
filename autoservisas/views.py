from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm
from .models import Automobilis, Uzsakymas, Paslauga
from .forms import AutomobilisReviewForm, UserUpdateForm, ProfilisUpdateForm, AutomobilisCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from django.views import generic
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

class AutomobilisDetailView(FormMixin, DetailView):
    model = Automobilis
    template_name = 'automobilis_detail.html'
    form_class = AutomobilisReviewForm

    def get_success_url(self):
        return reverse('automobilis-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.automobilis = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(AutomobilisDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get('query')
    automobiliai = Automobilis.objects.filter(automobilio_modelis__marke__icontains=query)
    return render(request, 'search.html', {'automobiliai': automobiliai, 'query': query})


class LoanedAutomobiliaiByUserListView(LoginRequiredMixin, generic.ListView):
    model = Automobilis
    template_name = 'user_automobiliai.html'
    paginate_by = 3

    def get_queryset(self):
        return Automobilis.objects.filter(reader=self.request.user).order_by('due_back')


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):

        reset_url = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', args=[form.cleaned_data['uid'], form.cleaned_data['token']])
        )

        print(f'Password reset link: {reset_url}')

        return super().form_valid(form)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)

class AutomobiliaiByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = Automobilis
    template_name = 'user_automobiliai.html'



class AutomobilisByUserCreateView(LoginRequiredMixin, CreateView):
    model = Automobilis
    fields = ['automobilio_modelis', 'due_back']
    success_url = '/autoservisas/myautomobiliai/'
    template_name = 'user_automobilis_form.html'
    form_class = AutomobilisCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    # Add this method to check if the user is allowed to create a new automobilis
    def test_func(self):
        return self.request.user.is_authenticated

class AutomobilisByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Automobilis
    fields = ['automobilio_modelis', 'due_back']
    success_url = "/autoservisas/myautomobiliai/"
    template_name = 'user_automobilis_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        automobilis = self.get_object()
        return self.request.user == automobilis.reader


class AutomobilisByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Automobilis
    template_name = 'user_automobilis_delete.html'

    def test_func(self):
        automobilis = self.get_object()
        return self.request.user == automobilis.reader

    def get_success_url(self):
        return reverse('my-borrowed')


class AutomobilisByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Automobilis
    form_class = AutomobilisCreateForm
    success_url = '/autoservisas/myautomobiliai/'
    template_name = 'user_automobilis_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)