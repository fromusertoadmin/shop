from .models import PrivacyPolicy


def get_privacy_policy(request):
    privacy_policy = PrivacyPolicy.objects.filter(is_active=True).last()
    return locals()
