### **AI Game Master**
🚀 **A Modular Flask API for AI-powered RPG Game Mastering** 🎲  

This project provides an **AI-powered Game Master** for tabletop RPGs. It supports **rule enforcement, narration, dice rolling, campaign management, player turns, sound effects, and more**. Users can upload **custom RPG rulebooks, scenarios, and sound effects** for a fully immersive experience.

---

## **📂 Project Structure**
```
ai_game_master/
│── app/
│   │── __init__.py       # Flask app initialization
│   │── routes.py         # API routes
│   │── config.py         # Configuration settings
│── models/
│   │── __init__.py       # Module initialization
│   │── game_master.py    # Handles turn order, campaigns, scenarios
│   │── utilities.py      # Dice rolling, rule enforcement, narration
│   │── sound_manager.py  # Handles sound uploads and retrieval
│── uploads/              # Directory for sound and rulebook uploads
│── run.py                # Entry point to run the Flask app
│── requirements.txt      # Dependencies
│── .gitignore            # Files to exclude from Git
│── README.md             # Documentation
```

---

## **🛠️ Features**
✅ **AI-Driven Game Master** – Narration, improvisation, and dynamic storytelling  
✅ **Dice Rolling** – Supports **d4, d6, d8, d10, d12, d20, d100**  
✅ **Turn-Based Play** – Moderates turns for single or multiplayer campaigns  
✅ **Campaign & Scenario Management** – Load prebuilt campaigns or upload custom scenarios  
✅ **Rule Enforcement** – AI checks actions against game rules  
✅ **Custom Rulebooks** – Upload PDFs to extract game mechanics  
✅ **Sound Effects & Music** – Upload, generate, and share audio  
✅ **Speech-to-Text Support** – Interact with the AI GM using voice commands  

---

## **Backend Functionality**
- **Flask API** for all game master features
- **API Endpoints:**
  - `/roll` – Dice rolling (supports standard dice notation)
  - `/narrate` – AI-powered narration and responses
  - `/upload_rulebook` – Upload custom rulebooks (PDF)
  - `/upload_sound` – Upload sound effects/music (MP3/WAV)
  - `/next_turn` – Advance to the next player's turn
- **Models:**
  - **Game Master:** Handles turn order, campaigns, and scenarios
  - **Utilities:** Dice rolling, rule enforcement, narration
  - **Sound Manager:** Handles sound uploads and retrieval
- **Uploads:** Stores user-uploaded rulebooks and sound files
- **Database:** Uses SQLAlchemy for campaign, character, and session management

## **Frontend Functionality**
- **Modern UI** (Vite + React)
- **Chat Panel:** Interact with the AI GM
- **Dice Panel:** Roll dice with UI controls
- **Character Sheet:** View and manage character info
- **Game Buttons:** Start new game, resume game, etc.
- **Live Updates:** UI reflects game state and turn order
- **Test Coverage:** Frontend and backend tests included

---

## **🖥️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/ai-game-master.git
cd ai-game-master
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Flask API**
```bash
python run.py
```
Your API will start at `http://127.0.0.1:5000`.

---

## **📡 API Endpoints**
### 🎲 **Dice Rolling**
```http
POST /roll
```
**Request Body:**
```json
{ "dice": "2d6" }
```
**Response:**
```json
{ "roll": [4, 3] }
```

---

### 🗣️ **Narration & AI Game Master**
```http
POST /narrate
```
**Request Body:**
```json
{ "prompt": "Describe an ancient ruin filled with traps." }
```
**Response:**
```json
{ "narration": "The ruins are overgrown with vines, hiding pressure plates and dart traps..." }
```

---

### 📜 **Upload a Custom Rulebook (PDF)**
```http
POST /upload_rulebook
```
**Request Body:**  
Upload a **PDF file** containing RPG rules.  

**Response:**
```json
{ "rules": "Extracted rules text from PDF..." }
```

---

### 🎵 **Upload Sound Effects & Music**
```http
POST /upload_sound
```
**Request Body:**  
Upload an **MP3/WAV** file.

**Response:**
```json
{ "message": "Sound 'battle_music.mp3' uploaded successfully.", "path": "uploads/battle_music.mp3" }
```

---

### 🔄 **Next Player's Turn**
```http
POST /next_turn
```
**Response:**
```json
{ "next_turn": "It's Alice's turn." }
```

---

## **📝 TODO / Future Improvements**
- [ ] Web-based interface for interactive play  
- [ ] Discord bot integration  
- [ ] More RPG system support  
- [ ] AI-generated dynamic encounters  

---

## **🤝 Contributing**
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-xyz`)  
3. Commit your changes (`git commit -m "Added feature xyz"`)  
4. Push to the branch (`git push origin feature-xyz`)  
5. Open a Pull Request  

---

## **📜 License**
MIT License. Feel free to use, modify, and distribute.

