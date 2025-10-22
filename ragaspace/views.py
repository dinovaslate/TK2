from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from allauth.exceptions import ProviderNotFound
from allauth.socialaccount.providers import registry

from .forms import EmailAuthenticationForm, RegistrationForm


def _build_social_login_urls(request, process: str) -> dict[str, str]:
    """Return enabled social login URLs for the requested process."""

    urls: dict[str, str] = {}
    for provider_id in ("google", "facebook", "apple"):
        try:
            provider = registry.by_id(provider_id, request)
        except ProviderNotFound:
            continue

        if provider is None:
            continue

        try:
            urls[provider_id] = provider.get_login_url(request, process=process)
        except Exception:  # pragma: no cover - provider-specific failures
            continue

    return urls


class EmailLoginView(LoginView):
    template_name = 'ragaspace/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('ragaspace:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_login_urls'] = _build_social_login_urls(self.request, process='login')
        return context


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
        'social_login_urls': _build_social_login_urls(request, process='login'),
        'social_signup_urls': _build_social_login_urls(request, process='signup'),
    })


@login_required
def dashboard(request):
    return render(request, 'ragaspace/dashboard.html')
