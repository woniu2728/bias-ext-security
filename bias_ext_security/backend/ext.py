from bias_ext_security.backend.extenders import (
    auth_extenders,
    frontend_extenders,
    lifecycle_extenders,
    settings_extenders,
)


def extend():
    return [
        *frontend_extenders(),
        *settings_extenders(),
        *auth_extenders(),
        *lifecycle_extenders(),
    ]
