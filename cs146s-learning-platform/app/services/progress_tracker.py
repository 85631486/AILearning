"""
Compatibility shim for ProgressTracker.

This module provides backward compatibility for imports from the old progress_tracker.py.
New code should import from app.services.progress_tracker instead.

DEPRECATED: This shim will be removed in a future version.
"""

from app.services.progress_tracker.service import ProgressTracker

# Export the class for backward compatibility
__all__ = ['ProgressTracker']
