# MindMate

**MindMate** is a supportive mental health companion web app. It features a friendly AI-powered chatbot, a personal mood tracker, curated mental health resources, and reminders to help you care for your wellbeing.

---

## Features

- **AI Chatbot:** Provides supportive conversation and information using Gemini AI.
- **Mood Tracker:** Log your daily moods and notes, visualize your emotional journey.
- **Resources:** Quick access to mental health helplines, guides, and articles.
- **Reminders:** (Planned) Set gentle reminders for self-care activities.
- **Responsive UI:** Beautiful, soothing design for desktop and mobile.

---

## Getting Started

### **1. Clone the repository**

```bash
git clone https://github.com/your-username/mindmate.git
cd mindmate
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Set up configuration**

Create a `.env` file (or set environment variables) for sensitive configs:

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///mindmate.db
GEMINI_API_KEY=your-gemini-api-key
```

Or edit `config.py` directly for local development.

### **4. Initialize the database**

```bash
python
>>> from app import models, create_app
>>> app = create_app()
>>> with app.app_context():
...     models.db.create_all()
```

### **5. Run the app locally**

```bash
python run.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deployment

Deploy easily to [Render](https://render.com):

1. Make sure `requirements.txt` and `render.yaml` are present.
2. Push your code to GitHub.
3. Connect your repo at Render and deploy.

---

## Project Structure

```
mindmate/
├── app/
│   ├── templates/      # HTML templates
│   ├── static/         # CSS, JS, images
│   ├── models.py       # SQLAlchemy models
│   ├── routes.py       # App routes
│   ├── gemini_api.py   # Gemini API integration
│   ├── utils.py        # Helper functions
├── run.py              # App entrypoint
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
└── README.md           # This file
```

---

## Customization

- **Add moods:** Edit `Mood.MOOD_CHOICES` in `models.py`.
- **Edit resources:** Update the list in `routes.py`.
- **Change styling:** Edit `app/static/css/style.css` and templates.

---

## Contributing

Pull requests and issue reports are welcome!
- Please be mindful of the mental health focus.
- All feedback and suggestions appreciated.

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Google Gemini AI](https://ai.google.dev/)
- [Render](https://render.com/)
- Inspiration: All who support mental wellness 💚

---

**You are not alone. MindMate is here for you.**
