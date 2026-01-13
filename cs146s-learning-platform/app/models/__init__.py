"""
CS146S Learning Platform - Data Models Package

This package contains all database models for the learning platform.
Models are organized into separate modules for better maintainability.
"""

from .user import User
from .week import Week
from .exercise import Exercise
from .submission import Submission
from .user_progress import UserProgress
from .ai_conversation import AIConversation
from .system_config import SystemConfig
from .autosave import AutoSave
from .assignment_file import AssignmentFile

# Export all models for backward compatibility
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
