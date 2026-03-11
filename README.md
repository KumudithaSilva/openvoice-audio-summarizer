# 🎙️✨ OpenVoice-Audio Summarizer

<p align="center">
  <img src="https://img.shields.io/badge/LLM-Falcon3-7B1FA2" />
  <img src="https://img.shields.io/badge/Speech%20Recognition-Whisper%20Medium-455A164" />
  <img src="https://img.shields.io/badge/Deep%20Learning-PyTorch-EE4C2C" />
  <img src="https://img.shields.io/badge/GPU-Acceleration-76B900" />
  <img src="https://img.shields.io/badge/Model-Quantization-3F51B5" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688" />
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF7043" />
  <img src="https://img.shields.io/badge/Design-SOLID%20Principles-17256b" />
  <img src="https://img.shields.io/badge/Code%20Style-PEP8-045E1A" />
  <img src="https://img.shields.io/badge/License-MIT-45a5d7" />
</p>


## 🎯 Overview

OpenVoice Audio Summarizer is an open-source platform designed to transform meeting recordings and audio files into concise summaries and actionable insights. The system helps improve meeting productivity by organizing key discussion points and reducing the time required to review recordings. It primarily operates using open-source end-to-end models, eliminating the need for external API services. As a result, the entire process runs locally on the user’s machine, ensuring zero API cost and better data privacy.

The OpenVoice Audio Summarizer is built using pre-trained models such as Falcon3 with 1 billion parameters and the Whisper Medium speech recognition model. Whisper is used to convert audio into text, while the Falcon model generates summaries and insights from the transcribed content.

To improve computational efficiency, the system runs on an NVIDIA GeForce RTX 2070 GPU. Additionally, 4-bit quantization is applied to the Falcon model to optimize memory usage and performance while maintaining model accuracy.


## ✨ Core Features

- Audio File Processing
- Audio File Preprocssing
- Automatic Transcription 
- Automatic Speech Recognition (ASR)
- Intent and Topic Detection
- Context-Aware Summarization
- Real Time Internal Logs
- Local Model Execution

## 📸 OpenVoice Audio Summarizer Output (UI Preview)

#### OpenVoice Log Output

<img width="500" height="700" alt="image" src="https://github.com/user-attachments/assets/213e99bb-c601-47df-899c-c9b019734003"/>


## 🏗️ Architecture

The system is follows a layered, interface-driven architecture, designed to ensure modularity, maintainability, and extensibility. Fundamental design principles include dependency injection, interface-based abstraction, separation of concerns, and a plugin-oriented tool architecture.

<b>Key Architectural Highlights:</b>
- Dependencies are injected via a centralized container, promoting loose coupling and easy testing.
- Core components define interfaces to enforcing contracts and enabling polymorphic behavior.
- Singleton patterns are used for global utilities like logging.
- The architecture defines clear layers: UI/API, Components (business logic), Infrastructure (integrations), Interfaces (contracts), and Container (dependency management).

```
┌─────────────────────────────────────┐
│       UI Layer (Streamlit)          │
│       Backend API (FastAPI)         │
├─────────────────────────────────────┤
│    Components (Business Logic)      │
│  ├─ Chat Generation Service         │
│  ├─ Chat Connection Service         │
│  ├─ Transcript Generation Service   │
│  └── Voice Connection Service       │
├─────────────────────────────────────┤
│    Infrastructure (Integrations)    │
│  ├─ FalconAI Service                │
|  ├─ WhisperAI Service               │
|  ├─ Audio Service                   │
│  ├─ Chat Prompt                     │
│  ├─ Environment & Configuration     │
│  └─ AI Models                       │
├─────────────────────────────────────┤
│    Interfaces (Contracts)           │
│  ├─ Chat Interfaces                 │
│  ├─ Audio Interfaces                │
│  ├─ Infrastructure Interfaces       │
│  ├─ Logging Interfaces              │
│  └─ LLM Interfaces                  │
├─────────────────────────────────────┤
│    Container (Dependency Injection) │
│    Dependency Wiring & Factory      │
├─────────────────────────────────────┤
│    Core (Utilities & Patterns)      │
│    Singleton Meta-class             │
└─────────────────────────────────────┘
```

### Layer Responsibilities

- <b>UI/API Layer</b>: Facilitates user interactions and exposes RESTful endpoints.
- <b>Components Layer</b>: Orchestrates business logic and AI-driven chat operations.
- <b>Infrastructure Layer</b>: Manages external integrations, Audio services, and system utilities.
- <b>Interfaces Layer</b>: Defines abstract contracts to ensure modularity and testability.
- <b>Container LayerL</b>: Oversees dependency injection and management of singleton instances.


## 📁 Project Structure

```
open-voice-audio-summarizer/
│
├── audio/                            # Audio files for testing
│   ├── meeting_audio.wav
│   └── team_meeting.mp3
│
├── backend/                          # FastAPI API Layer
│   ├── dependencies/                 # Dependency providers for routes
│   │   └── dependencies.py
│   │
│   ├── routes/                       # API endpoints
│   │   └── chat.py
│   │
│   └── main.py                       # FastAPI app initialization with lifespan
│
├── src/                              # Application Core Layer
│   ├── dto/                          # Internal DTOs (service layer contracts)
│   │   └── audio_data.py             # Audio data representation
│   │
│   │
│   ├── components/                   # Business logic orchestration
│   │   ├── chat_generation.py        # summary generation
│   │   ├── chat_connection.py        # falcon3 client management
│   │   ├── voice_transcription.py    # audio to raw text generation
│   │   └── voice_connection.py       # whisper client management
│   │
│   │
│   ├── container/                    # Dependency Injection
│   │   └── openvoice_container.py    # Factory for FalconAI and WhisperAI
│   │
│   │
│   ├── core/                         # Core utilities
│   │   └── singleton_meta.py         # Singleton pattern implementation
│   │
│   │
│   ├── infrastructure/                # External integrations
│   │   ├── falconai_service.py        # Falcon3 client wrapper
│   │   ├── falconai_client.py         # Low-level FalconAI integration
│   │   ├── whisperai_service.py       # Whisper client wrapper
│   │   ├── whisperai_client.py        # Low-level WhisperAI integration
│   │   ├── falcon_prompt.py           # Prompt management
│   │   ├── config_provider.py         # Configuration loader
│   │   └── audio_processor.py         # Audio preprocessing services
│   │
│   ├── interfaces/                          # Abstract contracts
│   │   ├── audio/                           # Audio interfaces
│   │   │   └── audio_service_interface.py
│   │   │
│   │   ├── chat/                            # Chat interfaces
│   │   │   └── chat_service_interface.py
│   │   │
│   │   ├── infra/                           # Infrastructure interfaces
│   │   │   └── config_provider_interface.py
│   │   │
│   │   ├── logging/                         # Logging interfaces
│   │   │   └── logger_interface.py
│   │   │
│   │   └── llm/                             # LLM interfaces
│   │       ├── falcon_interface.py
│   │       └── whisper_interface.py
│   │
│   │
│   └── logs/
│       ├── logger_singleton.py        # Singleton logger
│       └── logger_streamlit.py        # Streamlit logger
│
│
├── ui/                                # Frontend Layer
│   └── app.py                         # Streamlit openvoice interface
│
│
├── config.yaml                        # Application configuration
├── setup.py                           # Package setup
├── requirements.txt                   # Dependencies
└── README.md                          # Documentation
```

  ## 🔄 How It Works

### Request Flow

```
User Upload Audio Input (Streamlit UI)
        │
        ▼
FastAPI Backend (async)
        │
        ├─► (/chat/user_upload)
        │   
        │
        ├─► (/chat/streamlit_logs)
        │   
        │
        ▼
OpenVoiceContainer ──────► VoiceConnectionService & ChatConnectionService
        │
        ├─► VoiceTranscriptionService
        │  	 (Create and return an audio transcription)
        │
        ├─► ChatGenerationService
        │   (Generation and retrun the audio summary)
        │
        ▼
AI Model & Audio Process
        │
        ├─► Audio Processor
        │      (Provide preprocess audio waveform)
        │      └─ Stream logs to UI
        │
        ├─► Whisper Audio Transcription
        │      (Transcribe audio data to text)
        │      └─ Stream logs to UI
        │
        ├─► Prompt Provider
        │      (Provide system prompts and user prompt with transcribed data)
        │      └─ Stream logs to UI
        │
        ├─► Falcon3 Text to Summary
        │      (Generate a response for given prompt)
        │      └─ Stream logs to UI
        │
        └─ If response generated:
        │        │
        │        └─► Return to UI
        │              ├─ Display final result to user
        │─────────►├─ Streaming logs continue

```

## 📌 Prerequisites

- A system with **GPU and CUDA** support  
- Minimum GPU memory: **6 GB**  
- **Conda** installed (for environment management)  
- **Python 3.10** recommended 

---

## 💻 Installation

1. Create a Conda environment:

```bash
conda create -n llm-openvoice python=3.10
```

2. Activate the environment:
```bash
conda activate llm-openvoice
```

3. Install PyTorch, TorchAudio, and CUDA support:
```bash
conda install pytorch torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

4. Install dependencies
```bash
pip install -r requirement.txt
```

5. Download required models:
- `Falcon3-1B-Instruct` → save to a local folder, e.g., G:/LLMs/Falcon3-1B-Instruct
  - Download `tiiuae/Falcon3-1B-Instruct`
- `Whisper-Medium` → save to a local folder, e.g., G:/LLMs/whisper_medium_en
  - Download `openai/whisper-medium.en`
- After downloading the models, update config.yaml with the paths where you saved the models

```yaml
models:
  Falcon3-1B-Instruct:
    location: "YOUR_LOCAL_PATH/Falcon3-1B-Instruct"
  Whisper-Medium:
    location: "YOUR_LOCAL_PATH/whisper_medium_en"
```

## 🤝 Contributing

We welcome contributions related to:

- Additional language support
- AI & Prompt Engineering  
- Architecture Improvements  
- Backend Enhancements  
- UI Improvements  
- Testing & Quality Assurance  

### Contribution Steps

1. 🍴 Fork the repository  
2. 🌿 Create a `feature/*` branch  
3. 🛠️ Commit changes with clear messages  
4. 📤 Open a Pull Request  


## 🔀 Git Flow Workflow

The project follows a Git Flow–inspired workflow:

- 🌿 `master` — Stable, production-ready releases  
- 🌱 `develop` — Active development branch  
- ✨ `feature/*` — New feature branches  

### Typical Workflow

1. Pull latest changes from `develop`  
2. Create a `feature/*` branch  
3. Implement and test changes  
4. Open PR → Merge into `develop`  
5. Release from `develop` → Merge into `master`  

This ensures stability while enabling safe feature development.

---

