   from flask import Blueprint, request, jsonify, render_template, session
from .groq_api import get_gpt_oss_response  # UPDATED IMPORT STATEMENT
from .models import db, Mood, ChatHistory
from .utils import get_current_user, crisis_detected

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@routes.route('/mood', methods=['GET', 'POST'])
def mood():
    user = get_current_user()
    if request.method == 'POST':
        mood_value = request.form.get('mood')
        note = request.form.get('note', '')
        if not mood_value:
            moods = Mood.MOOD_CHOICES
            moods_history = Mood.query.filter_by(user_id=user.id).order_by(Mood.timestamp.desc()).limit(30).all()
            return render_template('mood.html', error="Please select your mood.", moods=moods, mood_history=moods_history)
        mood_entry = Mood(user_id=user.id, mood=mood_value, note=note)
        db.session.add(mood_entry)
        db.session.commit()
        moods = Mood.MOOD_CHOICES
        moods_history = Mood.query.filter_by(user_id=user.id).order_by(Mood.timestamp.desc()).limit(30).all()
        return render_template('mood.html', success="Mood logged!", moods=moods, mood_history=moods_history)
    # GET: Show mood history
    moods = Mood.MOOD_CHOICES
    moods_history = Mood.query.filter_by(user_id=user.id).order_by(Mood.timestamp.desc()).limit(30).all()
    return render_template('mood.html', moods=moods, mood_history=moods_history)

@routes.route('/chat', methods=['POST'])
def chat():
    user = get_current_user()
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message received"}), 400

    # Store user message in chat history
    chat_entry = ChatHistory(user_id=user.id, sender='user', message=user_message)
    db.session.add(chat_entry)
    db.session.commit()

    # Detect crisis keywords
    if crisis_detected(user_message):
        crisis_response = (
            "It seems you may be experiencing a crisis. "
            "Please consider reaching out to a mental health professional or calling an emergency helpline immediately."
        )
        chat_entry_bot = ChatHistory(user_id=user.id, sender='bot', message=crisis_response)
        db.session.add(chat_entry_bot)
        db.session.commit()
        return jsonify({"response": crisis_response, "crisis": True})

    # Get GPT-OSS response from Groq API
    bot_response = get_gpt_oss_response(user_message)  # UPDATED FUNCTION CALL
    chat_entry_bot = ChatHistory(user_id=user.id, sender='bot', message=bot_response)
    db.session.add(chat_entry_bot)
    db.session.commit()
    return jsonify({"response": bot_response})

@routes.route('/chat/history', methods=['GET'])
def chat_history():
    user = get_current_user()
    history = ChatHistory.query.filter_by(user_id=user.id).order_by(ChatHistory.timestamp.desc()).limit(50).all()
    return jsonify([
        {"sender": h.sender, "message": h.message, "timestamp": h.timestamp.isoformat()}
        for h in reversed(history)
    ])

@routes.route('/resources', methods=['GET'])
def resources():
    resources_list = [
        {"title": "National Helpline", "url": "tel:18002738255"},
        {"title": "Mindfulness Meditation Guide", "url": "https://www.mindful.org/how-to-meditate/"},
        {"title": "Mental Health Articles", "url": "https://www.psychologytoday.com/us/topics/mental-health"},
    ]
    return jsonify(resources_list)

@routes.route('/reminders', methods=['POST'])
def set_reminder():
    # Placeholder: would require a Reminder model and scheduling
    data = request.json
    reminder_text = data.get("reminder")
    reminder_time = data.get("time")
    # Save to DB & schedule logic here
    return jsonify({"success": True, "message": "Reminder set!"})

@routes.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@routes.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500
