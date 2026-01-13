"""
CS146S Learning Platform - Models Compatibility Layer

This file provides backward compatibility for imports from the old monolithic models.py.
New code should import from app.models package instead.

DEPRECATED: This shim will be removed in a future version.
"""

# Import all models from the new package structure for backward compatibility
from app.models import (
    User,
    Week,
    Exercise,
    Submission,
    UserProgress,
    AIConversation,
    SystemConfig,
    AutoSave,
    AssignmentFile
)

# Export all models to maintain the same interface
__all__ = [
    'User',
    'Week',
    'Exercise',
    'Submission',
    'UserProgress',
    'AIConversation',
    'SystemConfig',
    'AutoSave',
    'AssignmentFile'
]