"""
Compatibility shim for AssignmentFileManager.

This module provides backward compatibility for imports from the old assignment_manager.py.
New code should import from app.services.assignment_manager instead.

DEPRECATED: This shim will be removed in a future version.
"""

from app.services.assignment_manager.service import AssignmentFileManager

# Export the class for backward compatibility
__all__ = ['AssignmentFileManager']
