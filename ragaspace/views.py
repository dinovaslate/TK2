from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from allauth.socialaccount.models import SocialApp

from .forms import EmailAuthenticationForm, RegistrationForm


def _build_social_login_urls(request, process: str) -> dict[str, str]:
    """Return enabled social login URLs for the requested process."""

    try:
        current_site = get_current_site(request)
    except Site.DoesNotExist:  # pragma: no cover - site misconfiguration
        current_site = None

    site_filter = {}
    if current_site is not None:
        site_filter = {"sites": current_site}
    elif getattr(settings, "SITE_ID", None) is not None:
        site_filter = {"sites__id": settings.SITE_ID}

    available_providers = set(
        SocialApp.objects.filter(provider__in=("google", "facebook", "apple"), **site_filter)
        .values_list("provider", flat=True)
    )

    urls: dict[str, str] = {}
    for provider_id in ("google", "facebook", "apple"):
        if provider_id not in available_providers:
            continue

        try:
            base_url = reverse("socialaccount_login", args=[provider_id])
        except Exception:  # pragma: no cover - URL configuration issues
            continue

        urls[provider_id] = f"{base_url}?process={process}"

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
