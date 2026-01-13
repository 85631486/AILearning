"""
Compatibility shim for SecureCodeExecutor.

This module provides backward compatibility for imports from the old code_executor.py.
New code should import from app.services.code_executor instead.

DEPRECATED: This shim will be removed in a future version.
"""

from app.services.code_executor.service import SecureCodeExecutor

# Export the class for backward compatibility
__all__ = ['SecureCodeExecutor']
