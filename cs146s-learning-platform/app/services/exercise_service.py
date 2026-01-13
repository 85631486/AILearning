"""
Compatibility shim for ExerciseService.

This module provides backward compatibility for imports from the old exercise_service.py.
New code should import from app.services.exercise_service instead.

DEPRECATED: This shim will be removed in a future version.
"""

from app.services.exercise_service.service import ExerciseService

# Export the class for backward compatibility
__all__ = ['ExerciseService']
