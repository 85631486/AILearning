"""
Compatibility shim for AIAssistant.

This module provides backward compatibility for imports from the old ai_assistant.py.
New code should import from app.services.ai_assistant instead.

DEPRECATED: This shim will be removed in a future version.
"""

from app.services.ai_assistant.service import AIAssistant

# Export the class for backward compatibility
__all__ = ['AIAssistant']
