### **AI Game Master**
🚀 **A Modular Flask API & React Frontend for AI-powered RPG Game Mastering** 🎲  

This project provides an **AI-powered Game Master** for tabletop RPGs. It supports **rule enforcement, narration, dice rolling, campaign management, player turns, sound effects, and more**. Users can upload **custom RPG rulebooks, scenarios, and sound effects** for a fully immersive experience.

---

## **📂 Project Structure**
```
backend/
│   app.py                # Flask app entry point
│   engine.py             # Core game logic and AI integration
│   gpt4_utils.py         # GPT-4 API helpers
│   models.py             # SQLAlchemy models
│   universe.py           # Universe/campaign logic
│   utils.py              # Dice, narration, rule enforcement
│   utils_embedding.py    # Embedding and search utilities
│
│── config/
│   config.py             # Configuration settings
│
│── routes/
│   api.py                # Main API endpoints
│   characters.py         # Character management endpoints
│   systems.py            # RPG system/rulebook endpoints
│   upload_rulebook.py    # Rulebook upload & parsing
│
│── tests/                # Backend test suite
frontend/
│   src/                  # React source code
│   public/               # Static assets
│   ...                   # Vite, config, and test files
instance/
│   dev.db                # SQLite database (dev)
migrations/               # Alembic DB migrations
requirements.txt          # Python dependencies
run_all_tests.sh          # Run all backend tests
README.md                 # Documentation
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
✅ **Modern Web UI** – React + Vite frontend for interactive play  
✅ **Test Coverage** – Backend and frontend tests included

---

## **Backend Functionality**
- **Flask API** for all game master features
- **API Endpoints:**
  - `/api/roll` – Dice rolling (standard dice notation)
  - `/api/narrate` – AI-powered narration and responses
  - `/api/upload_rulebook` – Upload custom rulebooks (PDF)
  - `/api/upload_sound` – Upload sound effects/music (MP3/WAV)
  - `/api/next_turn` – Advance to the next player's turn
  - `/api/characters` – Character management
  - `/api/systems` – RPG system/rulebook management
- **Models:**
  - **Game Master/Universe:** Handles turn order, campaigns, and scenarios
  - **Utilities:** Dice rolling, rule enforcement, narration
  - **Sound Manager:** Handles sound uploads and retrieval
- **Uploads:** Stores user-uploaded rulebooks and sound files
- **Database:** Uses SQLAlchemy for campaign, character, and session management
- **Testing:** Pytest-based suite in `backend/tests/`

## **Frontend Functionality**
- **Modern UI** (Vite + React)
- **Chat Panel:** Interact with the AI GM
- **Dice Panel:** Roll dice with UI controls
- **Character Sheet:** View and manage character info
- **Game Buttons:** Start new game, resume game, etc.
- **Live Updates:** UI reflects game state and turn order
- **Test Coverage:** Frontend tests included

---

## **🖥️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/ai-game-master.git
cd ai-game-master
```

### **2️⃣ Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
pip install -r ../requirements.txt
```

### **3️⃣ Run the Flask API**
```bash
python app.py
```
Your API will start at `http://127.0.0.1:5000`.

### **4️⃣ Frontend Setup (Optional)**
```bash
cd ../frontend
npm install
npm run dev
```
The frontend will start at `http://localhost:5173` (default Vite port).

---

## **📡 API Endpoints**
### 🎲 **Dice Rolling**
```http
POST /api/roll
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
POST /api/narrate
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
POST /api/upload_rulebook
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
POST /api/upload_sound
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
POST /api/next_turn
```
**Response:**
```json
{ "next_turn": "It's Alice's turn." }
```

---

## **📝 TODO / Future Improvements**
- [ ] Discord bot integration  
- [ ] More RPG system support  
- [ ] AI-generated dynamic encounters  
- [ ] Enhanced web-based interface  
- [ ] Cloud deployment scripts  

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

