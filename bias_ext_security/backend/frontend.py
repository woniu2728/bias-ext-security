from __future__ import annotations

from bias_core.extensions import FrontendExtender


def frontend_extender():
    return FrontendExtender(
        admin_entry="extensions/security/frontend/admin/index.js",
        forum_entry="extensions/security/frontend/forum/index.js",
    )
