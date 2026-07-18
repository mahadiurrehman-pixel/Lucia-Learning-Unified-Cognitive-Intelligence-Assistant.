# 🤖 LUCIA v0.2

### Learning Unified Cognitive Intelligence Assistant

> *"An AI companion that learns, adapts, and grows with you."*

![Version](https://img.shields.io/badge/Version-0.2_Beta-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Ollama](https://img.shields.io/badge/Ollama-llama3.2-orange)
![NLP](https://img.shields.io/badge/NLP-TextBlob+ArgosTranslate-purple)

---

## 📖 Table of Contents

- [What is LUCIA?](#-what-is-lucia)
- [What's New in v0.2](#-whats-new-in-v02)
- [Features](#-features)
- [Installation](#️-installation)
- [How to Run](#-how-to-run)
- [How to Use](#-how-to-use)
- [Project Structure](#-project-structure)
- [Commands](#️-commands-reference)
- [Limitations](#️-limitations)
- [Roadmap](#️-roadmap)
- [Developer](#-developer)

---

## 🌟 What is LUCIA?

LUCIA is a **personal AI assistant** built entirely in Python.
It is designed to learn about you over time and assist you
with your daily work and personal tasks.

Unlike static chatbots, LUCIA **remembers** what you tell her,
**adapts** to your workflow, **detects your emotions**, and now
**thinks intelligently** using a local LLM (Ollama).

### Core Philosophy:

> LUCIA starts as a general AI assistant,
> then adapts to each user's workflow,
> preferences, and knowledge over time.

### What Makes LUCIA Different:

✅ She remembers you across sessions  
✅ She learns your company workflow  
✅ She detects your emotions  
✅ She now speaks using a real AI brain (Ollama LLM)  
✅ She understands Hinglish, English, Urdu & more  
✅ She translates other languages automatically  
✅ Everything stored locally — your data stays private  
✅ No internet required (fully offline)

---

## 🆕 What's New in v0.2

| Feature | Details |
|---------|---------|
| 🧠 **Ollama LLM Integration** | llama3.2:3b model connected. Real intelligent responses. Context-aware conversation. |
| 🌍 **Multi-Language Support** | Hinglish, English, Urdu, Arabic, French, Spanish + more. Auto-detection & translation. |
| 🔤 **Fuzzy Matching** | Typo tolerance added. `"halp"` → detects as `"help"`. `"stresed"` → detects emotion. |
| 📜 **Conversation History** | Last 6 messages remembered. Ollama uses full context. Better follow-up responses. |
| 🌐 **ArgosTranslate** | Offline translation engine. Urdu/Arabic → English auto. No Google Translate needed. |
| 💬 **Smarter Emotion Detection** | Fuzzy + keyword + TextBlob. Combined scoring system. More accurate detection. |
| 🔒 **Safe Shutdown** | Goodbye saves properly. No data loss on exit. Clean shutdown sequence. |
| ⚡ **WAL Database Mode** | Faster SQLite writes. Safer concurrent access. Better performance. |

---

## ✅ Features

### 🧠 Memory System (SQLite Database)

**SAVE:**
- 👤 Personal info → name, age, email, city, phone
- 💼 Work info → company, profession, role
- ❤️ Preferences → hobbies, likes, dislikes
- 📚 Knowledge → workflow, rules, processes
- 💬 Conversations → full chat history stored

**RETRIEVE:**
- Ask for saved info anytime
- Search through all memories
- View memory status report

**DELETE:**
- Remove specific memories on command

### 🤖 Ollama AI Brain *(NEW in v0.2)*

- Powered by **llama3.2:3b** (local LLM)
- Understands context from conversation history
- Uses your saved memories for personalized answers
- Uses learned knowledge in responses
- Responds in Hinglish automatically
- Falls back gracefully if Ollama is offline

### 🌍 Multi-Language Support *(NEW in v0.2)*

| Language | Detection Method |
|----------|------------------|
| Hinglish | Custom keyword markers |
| English | Default |
| Urdu Script | Unicode character detection |
| Arabic | Arabic-specific character set |
| French | langdetect library |
| Spanish | langdetect library |
| Roman Urdu | Custom marker dictionary |

**Translation:**
- Non-English text → auto translated to English
- ArgosTranslate used (fully offline)
- Translation cached for performance

### 🎯 Intent Detection (14+ Intents)

| Intent | Trigger Example |
|--------|-----------------|
| greeting | "hello", "hi", "salam" |
| name_tell | "My name is Alex" |
| name_ask | "What is my name?" |
| memory_ask | "What do you remember?" |
| memory_delete | "Forget my age" |
| teach | "Our workflow is..." |
| help | "help" |
| status | "status" |
| goodbye | "bye", "exit" |
| thanks | "thanks", "shukriya" |
| personal_info | "My age is 22" |
| productivity | "I have a deadline" |
| general | Ollama handles this now ✨ |

### 😊 Emotion Detection *(Enhanced in v0.2)*

| Emotion | Detection Method |
|---------|------------------|
| Stressed | Keywords + Fuzzy + TextBlob |
| Happy | Keywords + Fuzzy + TextBlob |
| Sad | Keywords + Fuzzy + TextBlob |
| Angry | Keywords + Fuzzy + TextBlob |
| Confused | Keywords + Fuzzy + TextBlob |
| Motivated | Keywords + Fuzzy + TextBlob |

**New in v0.2:**
- Fuzzy matching catches typos
- TextBlob sentiment analysis added
- Multi-language emotion detection
- Combined scoring for accuracy

### 📚 Learning System

**Process:**

1. **User shares information**
   `"Our company workflow is: design → code → test"`
2. **LUCIA identifies the topic (30+ categories)**
   `Topic: "company_workflow"`
3. **LUCIA asks for confirmation**
   `"Should I save this? (haan/nahi)"`
4. **User confirms → Saved permanently**
   User declines → Discarded

**Categories include:**
workflow, company, team, project, rule,
schedule, tool, deadline, meeting, client,
product, support, training, marketing,
sales, hr, finance, security, technology,
and 15+ more.

### 💡 Productivity Assistant

**When stressed:**
- Top 3 priorities technique
- Pomodoro method (25min focus + 5min break)
- Task breakdown strategy
- Breathing exercises
- Motivational support

**When normal:**
- Task prioritization tips
- Time management advice
- Focus techniques
- Daily review system

### 🔒 Data Privacy

✅ Everything stored locally on your machine  
✅ SQLite database (lucia.db file)  
✅ No cloud, no internet, no external servers  
✅ Ollama runs 100% offline  
✅ Translation runs 100% offline (ArgosTranslate)  
✅ Your data never leaves your computer

---

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Terminal / Command Prompt
- Ollama (optional but recommended)

### Step 1 — Check Python Version

```bash
python --version
# Should show Python 3.7+
```

### Step 2 — Download LUCIA Files

Make sure you have these files in one folder:

```
LUCIA/
├── main.py
├── memory.py
├── personality.py
├── nlp_engine.py
├── learning.py
└── config.json
```

### Step 3 — Install Dependencies

```bash
pip install textblob
pip install langdetect
pip install argostranslate
pip install rapidfuzz
pip install ollama
```

Or install all at once:

```bash
pip install textblob langdetect argostranslate rapidfuzz ollama
```

### Step 4 — Download NLP Data

```bash
python -m textblob.download_corpora
```

### Step 5 — Install Ollama (Recommended)

```bash
# Windows / Mac / Linux
# Visit: https://ollama.com/download
# Download and install Ollama

# Then pull the model:
ollama pull llama3.2:3b
```

### Step 6 — Verify config.json

```json
{
    "name": "LUCIA",
    "full_name": "Learning Unified Cognitive Intelligence Assistant",
    "version": "0.2",
    "tone": "professional_friendly",
    "purpose": "work assistant that learns and adapts",
    "learning_mode": true,
    "language": "hinglish",
    "creator": "Mahadi",
    "settings": {
        "auto_save_memory": true,
        "confirm_before_learning": true,
        "show_emotion_detection": true,
        "max_memory_results": 5
    }
}
```

**That's it! You're ready. ✅**

---

## 🚀 How to Run

### Method 1 — Simple (Recommended)

```bash
cd "path/to/your/LUCIA/folder"
python main.py
```

### Method 2 — Full Python Path

```bash
# Windows
C:/Users/YourName/AppData/Local/Programs/Python/Python3XX/python.exe main.py

# Mac/Linux
python3 main.py
```

### Method 3 — Windows Batch File

Create a file called `run_lucia.bat`:

```bat
@echo off
cd /d "D:\Your\LUCIA\Folder"
python main.py
pause
```

Double-click `run_lucia.bat` to start LUCIA instantly!

### Successful Startup Output:

```
============================================================
  LUCIA initializing.....
============================================================

[PERSONALITY] : Config loaded from config.json
[NLP] Upgraded NLP Engine initialized!
[LEARNING] Learning system initialized!
[LUCIA] ✅ Ollama connected!

============================================================
  LUCIA V 0.2 is ready
============================================================

LUCIA: Welcome! 🚀 Main Lucia hoon — Learning Unified
       Cognitive Intelligence Assistant.
       Tumhara naam kya hai? ✨

You: _
```

### Without Ollama:

```
[LUCIA] ⚠️ Ollama not found — fallback mode active
```

LUCIA will still work! Just without AI responses.
All memory, learning, and intent features work normally.

---

## 💬 How to Use

### First Time — Tell LUCIA Your Name

```
You   : My name is Alex
LUCIA : Welcome aboard, Alex! 🚀
        Lucia ne tumhara naam yaad rakh liya. 🧠✨
        Ab batao, aaj kya karein?
```

### Save Personal Information

```
You   : My age is 25
LUCIA : ✅ Yaad rakh liya! Saved: age = 25

You   : I work at Google
LUCIA : ✅ Yaad rakh liya! Saved: company = Google

You   : My email is alex@gmail.com
LUCIA : ✅ Yaad rakh liya! Saved: email = alex@gmail.com

You   : I live in New York
LUCIA : ✅ Yaad rakh liya! Saved: city = New York
```

### Chat in Hinglish *(NEW)*

```
You   : yaar bohot stress hai aaj
LUCIA : 😟 Lag raha hai tum thode stressed ho.
        Koi baat nahi, Lucia tumhare sath hai!

        Ye try karo:
        🎯 Aaj ke top 3 priorities likho.
        ⏰ 25 min focus, 5 min break — Pomodoro!
        😌 5 deep breaths lo. Phir shuru karte hain.
```

### Ask General Questions (Ollama)

```
You   : Python mein list aur tuple ka difference kya hai?

LUCIA : [Ollama responds in Hinglish with explanation]
        List mutable hoti hai — matlab tum baad mein
        values change kar sakte ho. Tuple immutable hai —
        ek baar banao to change nahi hoti.
        Koi specific use case hai jismein help chahiye?
```

### Teach LUCIA Your Workflow

```
You   : hamara workflow ye hai: pehle design, phir code,
        phir testing

LUCIA : 📚 Main ne ye samjha:

        Topic: company_workflow
        Info : hamara workflow ye hai: pehle design,
               phir code, phir testing

        Kya ye sahi hai? Save kar lun? (haan/nahi)

You   : haan
LUCIA : ✅ Seekh liya! 'company_workflow' save ho gaya.
```

### Check Memories

```
You   : tumhe kya yaad hai?
LUCIA : Mujhe ye sab yaad hai:

        📁 PERSONAL_INFO:
           • name  : Alex
           • age   : 25
           • email : alex@gmail.com
           • city  : New York

        📁 LEARNED_KNOWLEDGE:
           • company_workflow : pehle design, phir code...
```

### Check Status

```
You   : status

LUCIA : ╔══════════════════════════════════════╗
        ║       🤖 LUCIA Status Report         ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║  📊 Memories     : 5                 ║
        ║  💬 Conversations: 12                ║
        ║  📚 Learned      : 2                 ║
        ║  👤 User         : Alex              ║
        ║  🧠 Ollama       : ✅ Active         ║
        ║  🟢 Status       : Active            ║
        ║                                      ║
        ╚══════════════════════════════════════╝
```

---

## 📁 Project Structure

```
LUCIA/
│
├── 📄 main.py              ← START HERE
│   Main controller
│   Ollama LLM integration
│   Conversation history manager
│   Decision making engine
│   Intent routing
│
├── 📄 memory.py
│   SQLite database manager (WAL mode)
│   3 tables: memories, conversations,
│             learned_knowledge
│   Save, retrieve, search, delete
│   Thread-safe connections
│
├── 📄 personality.py
│   LUCIA's personality definition
│   Response templates
│   Greeting generator (random)
│   Emotion-based responses
│   Help guide
│
├── 📄 nlp_engine.py
│   Upgraded NLP Engine
│   Multi-language detection
│   Hinglish / Roman Urdu detection
│   ArgosTranslate (offline translation)
│   Fuzzy emotion matching (rapidfuzz)
│   14+ intent patterns (regex)
│   Information extraction
│   TextBlob sentiment analysis
│
├── 📄 learning.py
│   Learning system
│   Topic identification (30+ categories)
│   Confirmation workflow (FIFO queue)
│   Knowledge storage
│
├── 📄 config.json
│   LUCIA settings
│   Name, tone, language, version
│   Feature toggles
│
└── 📄 lucia.db             ← Auto-generated
    SQLite database (WAL mode)
    All your data stored here
    Created automatically on first run
```

---

## ⌨️ Commands Reference

### Memory Commands

| What You Say | What LUCIA Does |
|--------------|-----------------|
| `"My name is [name]"` | Saves your name |
| `"What is my name?"` | Tells your name |
| `"My age is [number]"` | Saves your age |
| `"My email is [email]"` | Saves your email |
| `"I work at [company]"` | Saves your company |
| `"I live in [city]"` | Saves your city |
| `"I love [thing]"` | Saves your preference |
| `"What do you remember?"` | Shows all memories |
| `"tumhe kya yaad hai?"` | Shows all memories |
| `"Forget [key]"` | Deletes that memory |
| `"bhool ja [key]"` | Deletes that memory |

### System Commands

| Command | Result |
|---------|--------|
| `help` | Shows help guide |
| `status` | Shows memory + Ollama status |
| `bye` | Shuts down gracefully |
| `exit` | Shuts down LUCIA |
| `quit` | Shuts down LUCIA |

### Learning Commands

| What You Say | What LUCIA Does |
|--------------|-----------------|
| `"Our workflow is..."` | Starts learning process |
| `"hamara workflow ye hai..."` | Starts learning (Hinglish) |
| `"Remember this..."` | Starts learning process |
| `"Our company policy is..."` | Starts learning process |
| `"haan"` / `"nahi"` | Confirms or rejects save |
| `"yes"` / `"no"` | Confirms or rejects save |

### Greeting Commands

| Command | Result |
|---------|--------|
| `hello` / `hi` / `hey` | Greeting response |
| `salam` / `assalam o alaikum` | Islamic greeting |
| `kaise ho` / `kya haal hai` | Hinglish greeting |
| `good morning` / `good evening` | Time-based greeting |

---

## ⚠️ Limitations

### NLP Limitations

| Issue | Workaround |
|-------|------------|
| Hinglish name extraction — `"Mera naam Mahadi ha"` ❌ | Use English: `"My name is Mahadi"` ✅ |
| Sarcasm not detected — `"Oh great, another bug"` may detect as happy | State emotions directly: `"I am frustrated"` ✅ |
| No real-time context — `"Who is he?"` type questions | Each session loads from DB. Be specific each time. |
| Argos first-time slow | First translation downloads language pack (~50MB). After that: instant. |

### System Limitations

❌ Single user only (no multi-user support)  
❌ Terminal/CMD only (no graphical interface)  
❌ No voice input or output  
❌ No file reading capability (PDF, Word, etc.)  
❌ No reminder or scheduling system  
❌ No mobile application  
❌ No cloud sync  
❌ Ollama requires ~2GB RAM for llama3.2:3b

### Best Practices

✅ **Use English for name input**
   `"My name is Alex"` ← Best result

✅ **Install Ollama for best experience**
   Without it: basic responses only
   With it: intelligent AI responses

✅ **Be clear and specific**
   `"My age is 22"` ← Works great
   `"I am 22 years old"` ← Also works

✅ **One task per message**
   Don't combine multiple requests

✅ **Respond clearly to confirmations**
   Only type `"haan"/"nahi"` or `"yes"/"no"`
   when asked to confirm learning

✅ **Keep Ollama running in background**
   `ollama serve` (run in separate terminal)

---

## 🗺️ Roadmap

### ✅ v0.1 — Alpha (Completed)

- ✅ SQLite memory system
- ✅ 14 intent detection
- ✅ 6 emotion categories
- ✅ Learning system with confirmation
- ✅ Personality and response templates
- ✅ Productivity tips
- ✅ Persistent data storage
- ✅ Debug mode (NLP analysis display)
- ✅ Graceful shutdown
- ✅ Error handling

### ✅ v0.2 — Beta (Current)

- ✅ Ollama LLM integration (llama3.2:3b)
- ✅ Multi-language support
- ✅ Hinglish / Roman Urdu detection
- ✅ ArgosTranslate (offline translation)
- ✅ Fuzzy matching (rapidfuzz)
- ✅ Conversation history (context memory)
- ✅ Improved emotion detection
- ✅ WAL mode database
- ✅ Safe shutdown fix
- ✅ History timing fix

### 🔮 v0.3 — Planned

- 🔮 Debug mode toggle (on/off switch)
- 🔮 Reminder and scheduling system
- 🔮 Task manager with priorities
- 🔮 Notes system
- 🔮 Conversation history viewer
- 🔮 Multiple intent per message
- 🔮 Better Hinglish name extraction
- 🔮 Memory export / import (JSON)
- 🔮 Custom Ollama model selection

### 🚀 v0.4 — Future

- 🚀 Graphical User Interface (GUI)
- 🚀 Voice input and output
- 🚀 Multi-user support
- 🚀 File reading (PDF, Word, Excel)
- 🚀 Calendar integration
- 🚀 Plugin / extension system

### 🎯 v1.0 — Goal

- 🎯 Full-featured AI personal assistant
- 🎯 Mobile application
- 🎯 Optional cloud sync
- 🎯 Multi-language full support
- 🎯 Custom personality configuration
- 🎯 Third-party integrations

---

## 🐛 Known Issues

| Bug | Status | Workaround |
|-----|--------|------------|
| Hinglish name not detected | Known | Use English input |
| Argos first run is slow | Known | Wait for pack download (one time only) |
| Ollama response delay | Known | Normal for local LLM (~2-5 seconds) |
| Debug always visible | Known | Will be toggle in v0.3 |
| Multiple Python versions conflict | Known | Use full Python path |

---

## 📦 Dependencies

| Package | Version | Type | Purpose |
|---------|---------|------|---------|
| textblob | 0.17.1+ | External | Sentiment Analysis |
| nltk | 3.9+ | External | TextBlob Backend |
| langdetect | 1.0.9+ | External | Language Detection |
| argostranslate | 1.9+ | External | Offline Translation |
| rapidfuzz | 3.0+ | External | Fuzzy String Matching |
| ollama | 0.1+ | External | Local LLM Integration |
| sqlite3 | built-in | Standard | Database Management |
| re | built-in | Standard | Regex Pattern Matching |
| json | built-in | Standard | Config File Parsing |
| os | built-in | Standard | File Operations |
| sys | built-in | Standard | System Operations |
| random | built-in | Standard | Random Selection |
| datetime | built-in | Standard | Timestamps |

**Install All Dependencies:**

```bash
pip install textblob langdetect argostranslate rapidfuzz ollama
python -m textblob.download_corpora
```

---

## 🧪 Testing

**Quick Test After Installation:**

```bash
python memory.py       # Test memory system
python personality.py  # Test personality
python nlp_engine.py   # Test NLP + language detection
python learning.py     # Test learning system
python main.py         # Run full LUCIA
```

**Test Conversation:**

```
You: hello
You: My name is Alex
You: My age is 25
You: I work at Google
You: tumhe kya yaad hai?
You: status
You: hamara workflow ye hai: design phir code phir test
You: haan
You: yaar bohot stress hai
You: Python kya hai?
You: help
You: bye
```

---

## 👨‍💻 Developer

```
Developer    : Mahadi
Project      : LUCIA AI Assistant
Version      : 0.2 Beta
Language     : Python 3.14
Database     : SQLite (WAL Mode)
NLP Library  : TextBlob + ArgosTranslate
LLM          : Ollama (llama3.2:3b)
Started      : 2026
Status       : Active Development
```

---

## 📝 License

```
MIT License

Copyright (c) 2026 Mahadi

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- Ollama team for the local LLM platform
- TextBlob team for NLP library
- ArgosTranslate for offline translation
- RapidFuzz for fuzzy matching
- Python SQLite3 community
- NLTK project for language tools
- Python open source community

---

## 📞 Support

If you encounter any issues:

1. Check the **Known Issues** section above
2. Make sure all dependencies are installed:
   ```bash
   pip install textblob langdetect argostranslate rapidfuzz ollama
   ```
3. Make sure Ollama is running:
   ```bash
   ollama serve  # (in a separate terminal)
   ```
4. Use full Python path if `python` command fails
5. Restart LUCIA — your data is always safe
6. Check that `config.json` exists in same folder

---

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         🤖 LUCIA v0.2 - Beta Release                     ║
║                                                          ║
║   "I learn from you. I remember for you.                 ║
║    I think for you. I grow with you." ✨                 ║
║                                                          ║
║   Built with ❤️  by Mahadi                               ║
║   Python | SQLite | Ollama | ArgosTranslate | 2026       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

*README.md — LUCIA v0.2 Documentation*
*Last Updated: 2026*
*Version: 0.2 Beta*
