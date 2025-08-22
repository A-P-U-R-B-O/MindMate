// MindMate - Global JS

// Chatbot logic
document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loader = document.getElementById('loader');

    function appendMessage(text, sender) {
        const div = document.createElement('div');
        div.className = sender === 'user' ? 'user-message' : 'bot-message';
        div.textContent = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showLoader(show) {
        if (loader) loader.style.display = show ? 'block' : 'none';
    }

    function sendUserMessage() {
        const msg = userInput.value.trim();
        if (!msg) return;
        appendMessage(msg, 'user');
        userInput.value = '';
        showLoader(true);

        fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        })
        .then(res => res.json())
        .then(data => {
            showLoader(false);
            if (data.response) {
                appendMessage(data.response, 'bot');
                if (data.crisis) {
                    appendMessage("If you are in immediate danger, please call your local emergency number.", 'bot');
                }
            } else {
                appendMessage("Sorry, something went wrong.", 'bot');
            }
        })
        .catch(() => {
            showLoader(false);
            appendMessage("Sorry, something went wrong.", 'bot');
        });
    }

    if (sendBtn && userInput) {
        sendBtn.onclick = sendUserMessage;
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendUserMessage();
            }
        });
    }

    // Mood selection logic
    let moodSelectBtns = document.querySelectorAll('.mood-choice');
    let moodInput = document.getElementById('mood-input');
    if (moodSelectBtns.length && moodInput) {
        moodSelectBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                moodSelectBtns.forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                moodInput.value = btn.getAttribute('data-mood');
            });
        });
    }

    // Mood form validation
    let moodForm = document.getElementById('mood-form');
    if (moodForm) {
        moodForm.addEventListener('submit', function(e){
            const mood = moodInput.value;
            if (!mood) {
                e.preventDefault();
                document.querySelector('.feedback')?.remove();
                const errorDiv = document.createElement('div');
                errorDiv.className = 'feedback error';
                errorDiv.textContent = 'Please select your mood.';
                this.appendChild(errorDiv);
            }
        });
    }

    // Add more JS for resources/reminders/etc as needed
});
