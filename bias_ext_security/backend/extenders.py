from __future__ import annotations

from bias_core.extensions import LifecycleExtender

from bias_ext_security.backend.auth_contracts import auth_extender
from bias_ext_security.backend.frontend import frontend_extender
from bias_ext_security.backend.settings_contracts import build_human_verification_settings_extender


def frontend_extenders():
    return (frontend_extender(),)


def settings_extenders():
    return (build_human_verification_settings_extender(),)


def auth_extenders():
    return (auth_extender(),)


def lifecycle_extenders():
    return (LifecycleExtender(),)
