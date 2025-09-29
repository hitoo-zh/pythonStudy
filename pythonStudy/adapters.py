from allauth.account.adapter import DefaultAccountAdapter
from django.http import Http404


class NoSignupAccountAdapter(DefaultAccountAdapter):
    """Account adapter that disables user signup/registration"""

    def is_open_for_signup(self, request):
        """Disable signup functionality"""
        return False

    def new_user(self, request):
        """Prevent new user creation"""
        raise Http404("User registration is not allowed")