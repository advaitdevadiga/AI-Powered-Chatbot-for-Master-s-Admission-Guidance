# 🎓 Study Abroad Guide

A web app that helps students choose between **MTech** and **MBA** and compare top colleges in **India, USA, Australia and Europe**, with an interactive world map and an AI career-guide chatbot.

![Home page](docs/screenshots/home.png)

## ✨ Features

- **Choose your path** – start by picking MTech or MBA.
- **Interactive world map** (Leaflet + OpenStreetMap) – click a region to see its top colleges.
- **8 country pages** – ranked college cards with photos, scores and links to official websites.
- **Study guide panel** on each page – exams, costs, scholarships, work visa rules, salaries and top sectors.
- **AI chatbot** – answers questions about MBA / MTech / MS. Uses a local AI model through [Ollama](https://ollama.com) and falls back to built-in answers when Ollama isn't running.

| College list | Chatbot |
|---|---|
| ![Colleges](docs/screenshots/college-list.png) | ![Chatbot](docs/screenshots/chatbot.png) |

## 🛠 Tech stack

| Layer | Technology |
|---|---|
| Front end | HTML, CSS, JavaScript |
| Map | Leaflet.js, OpenStreetMap |
| Back end | Python, Flask, Flask-CORS |
| AI | Ollama with the `tinyllama` model (optional) |

## 🚀 Run it locally

### Windows (easiest)
1. Install [Python](https://www.python.org/downloads/) – tick **"Add python.exe to PATH"**.
2. Download or clone this repository.
3. Double-click **`start.bat`**. Your browser opens `http://localhost:5000`.

### Mac / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open <http://localhost:5000>.

### Optional: real AI answers
```bash
# 1. Install Ollama from https://ollama.com/download
# 2. Download the model
ollama pull tinyllama
# 3. Keep Ollama running and start the app
```
Without Ollama the chatbot still replies with basic built-in answers.

## 📁 Project structure

```
study-abroad-guide/
├── app.py              # Flask server: serves the site + /chat API
├── start.bat           # One-click launcher for Windows
├── requirements.txt    # Python dependencies
├── index.html          # Home page (choose MTech / MBA)
├── map.html            # Interactive world map
├── chatbot.html        # Chatbot page
├── countries/          # 8 pages: {india,usa,australia,europe}-{mtech,mba}.html
├── css/                # Stylesheets
├── js/chatbot.js       # Chat logic (sends messages to /chat)
├── Photos/             # College images
└── docs/screenshots/   # Images used in this README
```

## ⚙️ How the chatbot works

1. The browser sends your question to `POST /chat`.
2. `app.py` forwards it to the local Ollama server (`localhost:11434`) with a system prompt.
3. The model's reply is returned as JSON and shown in the chat window.
4. If Ollama is unavailable, a keyword-based fallback answers instead.

## ⚠️ Notes

- Rankings, costs and salaries are **approximate, hand-entered values** for guidance only. Always check official university websites.
- College photos are used for this educational project; replace them with images you have rights to before commercial use.
- The map needs an internet connection.

## 👤 Author

**YOUR NAME** – 6th semester mini project
GitHub: [@your-username](https://github.com/your-username)
