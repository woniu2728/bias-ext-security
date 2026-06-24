from django.apps import AppConfig

class SecurityExtensionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bias_ext_security.backend"
    label = "security"
