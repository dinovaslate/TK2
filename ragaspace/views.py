from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import EmailAuthenticationForm, RegistrationForm


class EmailLoginView(LoginView):
    template_name = 'ragaspace/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('ragaspace:dashboard')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('ragaspace:login')


def register(request):
    if request.user.is_authenticated:
        return redirect('ragaspace:dashboard')

    form = RegistrationForm(request.POST or None)
    login_form = EmailAuthenticationForm(request=request)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        auth_login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('ragaspace:dashboard')

    return render(request, 'ragaspace/register.html', {
        'form': form,
        'login_form': login_form,
    })


@login_required
def dashboard(request):
    return render(request, 'ragaspace/dashboard.html')
