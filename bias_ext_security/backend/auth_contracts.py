from __future__ import annotations

from bias_core.extensions import AuthExtender

from bias_ext_security.backend.human_verification import verify_human_verification


def auth_extender():
    return AuthExtender().human_verification(
        "turnstile",
        verify_human_verification,
        description="在登录和注册流程中校验 Cloudflare Turnstile token。",
    )
