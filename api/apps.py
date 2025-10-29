from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # Import signal handlers
        import api.signals

        # Do the patch safely
        try:
            from rest_framework.views import APIView
            from api.signals import set_current_user

            # Keep reference to original method
            _original_initialize_request = APIView.initialize_request

            def _initialize_request_with_user(self, request, *args, **kwargs):
                req = _original_initialize_request(self, request, *args, **kwargs)
                if req.user and req.user.is_authenticated:
                    set_current_user(req.user)
                return req

            APIView.initialize_request = _initialize_request_with_user

        except ImportError:
            # DRF might not be installed or not used (e.g., during some migrations)
            pass