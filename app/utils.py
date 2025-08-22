from flask import session
from .models import User
import re

def get_current_user():
    """
    Retrieve the current user from the session.
    For demo: fallback to a default user. Replace with proper authentication in production.
    """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return user
    # In development, return the first user or create a demo user.
    user = User.query.first()
    if not user:
        user = User(username="demo_user")
        from .models import db
        db.session.add(user)
        db.session.commit()
    return user

def crisis_detected(message):
    """
    Detect if the message contains crisis keywords.
    Returns True if a crisis is detected, else False.
    """
    crisis_keywords = [
        r"\bsuicide\b", r"\bkill myself\b", r"\bend my life\b", r"\bhurt myself\b", r"\bdie\b",
        r"\bcan't go on\b", r"\bno hope\b", r"\bworthless\b", r"\bhelpless\b", r"\bself-harm\b",
        r"\bjump off\b", r"\boverdose\b", r"\bslit\b", r"\bdrown\b"
    ]
    message_lower = message.lower()
    for pattern in crisis_keywords:
        if re.search(pattern, message_lower):
            return True
    return False

def validate_mood(mood):
    """
    Validate if the provided mood is in the allowed choices.
    """
    from .models import Mood
    return mood in Mood.MOOD_CHOICES

def format_timestamp(dt):
    """
    Format datetime object to readable string for UI.
    """
    if not dt:
        return ""
    return dt.strftime('%Y-%m-%d %H:%M')
  
