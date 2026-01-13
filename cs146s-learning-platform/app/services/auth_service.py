"""
Compatibility shim for AuthService.

This module provides backward compatibility for imports from the old auth_service.py.
New code should import from app.services.auth_service instead.

DEPRECATED: This shim will be removed in a future version.
"""

from app.services.auth_service.service import AuthService

# Export the class for backward compatibility
__all__ = ['AuthService']
