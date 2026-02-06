# ⚡ The Keginator: The Web3 AI Data Utility

<div align="center">

<img src="public/logo.png" alt="The Keginator Logo" width="40px" style="margin-bottom:15px;"/>

<p>
<a href="https://github.com/JaimeCabary/The-keginator">
<img src="https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge" alt="Build"/>
</a>

<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
</a>

<a href="https://fastapi.tiangolo.com/">
<img src="https://img.shields.io/badge/FastAPI-ready-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
</a>

<a href="https://reactjs.org/">
<img src="https://img.shields.io/badge/React-Typescript-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
</a>

<a href="https://nextjs.org/">
<img src="https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js"/>
</a>

<a href="https://solana.com/">
<img src="https://img.shields.io/badge/Solana-supported-00FFA3?style=for-the-badge&logo=solana&logoColor=white" alt="Solana"/>
</a>

<a href="https://ai.google.dev/">
<img src="https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI"/>
</a>

<a href="LICENSE">
<img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="MIT License"/>
</a>
</p>

<p>
<a href="https://keginator.vercel.app">
<img src="https://img.shields.io/badge/🚀 Launch%20App-Click%20Here-orange?style=for-the-badge" alt="Launch App"/>
</a>
</p>

</div>

---

## 📑 Table of Contents

- [Overview](#overview)
- [Origin Story](#-our-origin-story-born-from-failure-built-for-speed)
- [Problem & Solution](#-problem--solution-summary)
- [Features](#-features)
- [AI Engine](#-the-ai-engine-cleaning-with-context)
- [Solana Trust Layer](#️-the-solana-trust-layer-why-web3-infrastructure)
- [Architecture](#-architecture)
- [Technical Stack](#-technical-stack)
- [Local Development Setup](#️-local-development-setup)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#1-backend-setup)
  - [Frontend Setup](#2-frontend-setup)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment-notes)
- [Project Gallery](#️-project-gallery-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [Security](#️-security--best-practices)
- [License](#️-license)
- [Acknowledgments](#️-acknowledgments)

---

## Overview

**The Keginator** is an AI-powered data preparation and provenance utility built to solve a simple, urgent problem: **data scientists and engineers should not lose time or hackathons because their data isn't ready.**

This application automates the massive human stress of preprocessing and cleaning datasets, then locks the integrity of that clean data onto the Solana blockchain, making it **provably trustworthy** at the lowest possible cost.

**Colosseum Hackathon Track: Infrastructure (Triton)**

---

## 🌟 Features

### 🤖 AI-Powered Data Cleaning
- **Intelligent Analysis**: Gemini AI analyzes your dataset structure and suggests optimal cleaning strategies
- **Automated Preprocessing**: Removes empty rows/columns, handles missing values, and normalizes data types
- **Context-Aware**: Maintains data context and relationships during cleaning
- **Multi-Format Support**: Works with CSV, JSON, XLSX, and audio files (MP3/WAV)

### ⛓️ Blockchain Provenance
- **Immutable Records**: Dataset hashes committed to Solana blockchain via Program Derived Addresses (PDAs)
- **Verification**: Anyone can verify dataset authenticity via hash lookup
- **Low Cost**: Minimal Solana gas fees for on-chain transactions
- **Tamper-Proof**: Cryptographic proof of data integrity

### 🎯 Developer Experience
- **FastAPI Backend**: High-performance async Python backend
- **React Frontend**: Modern, responsive TypeScript UI
- **RESTful API**: Clean, documented API endpoints
- **Real-time Processing**: Stream processing for large datasets
- **Comprehensive Logging**: Detailed operation logs for debugging

### 🔒 Authentication & Security
- **Google OAuth**: Easy sign-in with Google accounts
- **JWT Tokens**: Secure session management
- **Password Hashing**: bcrypt encryption for stored passwords
- **User Management**: Track dataset history per user

### 🎤 Multimodal Processing
- **Audio Transcription**: Faster-Whisper integration for MP3/WAV files
- **Text Embedding**: Sentence transformers for semantic analysis
- **Multiple Formats**: CSV, JSON, XLSX, and audio file support

---

## 💡 Our Origin Story: Born from Failure, Built for Speed

This entire project was born out of frustration. I recently lost a major Kaggle hackathon—a chance to fine-tune the Gemini 2.5 LLM—because I couldn't get my dataset ready on time.  
That failure showed me the painful truth: the stress of urgent data cleaning is a universal bottleneck.

The Keginator is my answer to that problem. It's built to help every machine learning person and data scientist bypass the stress of preprocessing and cleaning their dataset.

---

## 🌟 Problem & Solution Summary

| Problem | Solution: The Keginator |
| :--- | :--- |
| **Time-to-Train Stress:** Preprocessing and cleaning datasets for LLM fine-tuning consumes up to 80% of a data scientist's time. | **AI Data Cleaner:** An integrated AI applies data science principles to preprocess, chunk, fine-tune, and clean the dataset in split seconds. |
| **Data Integrity & Trust:** No verifiable method to prove a dataset was properly cleaned or remains untampered. | **Solana Provenance:** The SHA-256 hash of the final, *cleaned* dataset is permanently committed to a **Solana Program Derived Address (PDA)** for immutable proof. |
| **Cost Barrier:** Traditional tools are expensive, limiting access to quality data prep. | **Free Public Utility:** The core service is free, requiring only minimal Solana gas fees for the on-chain commitment transaction. |

---

## 🧠 The AI Engine: Cleaning with Context

The Keginator is not a simple script that removes bad data — it is a smart utility that does the complex work for you:

* **Contextual Reasoning:** The integrated AI reasons based on the context and structure of your data.  
* **Data Science Principles:** It applies preprocessing, normalization, scaling, and chunking methods automatically.  
* **Integrity Focused:** It ensures preprocessing without stripping context, preparing datasets for optimal LLM and ML use.  
* **Current Support:** Fully functional with **CSV** and **PDF** datasets.  

---

## ⛓️ The Solana Trust Layer: Why Web3 Infrastructure?

Once the AI produces a clean dataset, how do you *trust* it?  
We secure that integrity using Solana:

* **The Commitment:** We take the SHA-256 hash of the final, **cleaned** dataset.  
* **The Immutability:** That hash is logged immutably to a **Solana PDA** through our Anchor program.  
* **The Cost:** The core service is **free**—you only pay Solana’s minimal gas fees for the on-chain transaction.  
* **The Verification:** Anyone can verify via the `/verify/{hash}` endpoint and confirm authenticity on-chain.  

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React + TypeScript + Next.js                             │  │
│  │  - Upload Interface  - Verification  - History Dashboard  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API (JSON)
┌──────────────────────────▼──────────────────────────────────────┐
│                      Backend Layer (FastAPI)                     │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌────────────┐ │
│  │   Data     │  │  Gemini AI │  │  Audio   │  │    Auth    │ │
│  │  Cleaner   │  │  Analysis  │  │ Whisper  │  │  (OAuth)   │ │
│  └────────────┘  └────────────┘  └──────────┘  └────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐  ┌──────▼──────┐  ┌───────▼────────┐
│   PostgreSQL   │  │   Solana    │  │   File Store   │
│   (Metadata)   │  │ (Hash PDA)  │  │  (Uploads +    │
│                │  │             │  │   Cleaned)     │
└────────────────┘  └─────────────┘  └────────────────┘
```

### Data Flow
1. **Upload**: User uploads dataset via React frontend
2. **Clean**: FastAPI processes with Gemini AI analysis
3. **Hash**: SHA-256 hash computed for cleaned dataset
4. **Commit**: Hash written to Solana blockchain (PDA)
5. **Store**: Metadata saved to PostgreSQL
6. **Verify**: Anyone can verify hash authenticity on-chain

---

## 💻 Technical Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Blockchain** | **Solana (Anchor / Rust)** | Immutable hash logging & verification via PDAs |
| **Backend** | **FastAPI (Python 3.10+)** | Async API server, data processing, AI integration |
| **AI Engine** | **Google Gemini AI** | Intelligent data analysis and cleaning suggestions |
| **Audio** | **Faster-Whisper** | Audio transcription for MP3/WAV files |
| **Database** | **PostgreSQL / SQLite** | Dataset metadata storage with fallback support |
| **Frontend** | **React + TypeScript** | Modern responsive UI with Next.js framework |
| **Data Processing** | **Pandas + NumPy** | DataFrame manipulation and transformation |
| **ML Libraries** | **scikit-learn + sentence-transformers** | Data normalization and semantic embeddings |
| **Authentication** | **JWT + Google OAuth** | Secure user authentication and session management |

---

## 🛠️ Local Development Setup

### Prerequisites

Ensure you have the following installed:
- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** and npm ([Download](https://nodejs.org/))
- **PostgreSQL** (Optional - SQLite fallback available)
- **Solana CLI** (Optional - for blockchain testing)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env with your API keys
# Required: GEMINI_API_KEY
# Optional: SOLANA_PRIVATE_KEY, DATABASE_URL, etc.
nano .env  # or use your preferred editor

# Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Frontend Setup

```bash
# From project root directory
npm install

# Run development server
npm run dev
```

The frontend will start at `http://localhost:3000`

### 3. Solana Program ID

The Keginator uses a deployed Solana program for hash commitment:

```ini
KEGINATOR_PROGRAM_ID = Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS
```

This program is deployed on Solana Devnet.

---

## 🔐 Environment Variables

Create a `backend/.env` file with the following variables:

### Required Variables

```bash
# Gemini AI API Key (Required for AI-powered cleaning)
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional Variables

```bash
# Solana Configuration (Optional - mock mode if not provided)
SOLANA_PRIVATE_KEY=your_base58_encoded_private_key
SOLANA_PUBLIC_KEY=your_public_key
KEGINATOR_PROGRAM_ID=Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS
SOLANA_RPC_URL=https://api.devnet.solana.com

# Database (Optional - falls back to SQLite)
DATABASE_URL=postgresql://keginator:password@localhost:5432/keginator

# Authentication (Optional - for production)
JWT_SECRET=your_secret_key_change_in_production
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FRONTEND_URL=http://localhost:3000

# Audio Processing (Optional)
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

### Getting API Keys

1. **Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Solana Keypair**: Run `solana-keygen new` (requires Solana CLI)
3. **Google OAuth**: Configure at [Google Cloud Console](https://console.cloud.google.com/)

---

## 📚 API Documentation

### Base URL
```
Local: http://localhost:8000
Production: https://keginator-api.render.com
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-06T14:30:00Z"
}
```

---

#### 2. Upload Dataset
```http
POST /upload?user_id={user_id}&auto_commit={true|false}
Content-Type: multipart/form-data
```

**Parameters:**
- `user_id` (required): User identifier
- `auto_commit` (optional): Auto-commit to Solana (default: true)
- `file` (required): CSV, JSON, XLSX, MP3, or WAV file

**Request Example:**
```bash
curl -X POST "http://localhost:8000/upload?user_id=user123&auto_commit=true" \
  -F "file=@dataset.csv"
```

**Response:**
```json
{
  "success": true,
  "message": "Dataset cleaned and committed to Solana",
  "dataset_id": "abc123...",
  "dataset_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "rows_original": 1000,
  "rows_cleaned": 950,
  "columns": 15,
  "cleaning_report": {
    "operations": ["removed_empty", "standardized_columns", ...],
    "ai_insights": ["Dataset contains mixed types in column 'age'", ...]
  },
  "solana_signature": "5J7Kq...",
  "committed_to_solana": true,
  "download_url": "/download/abc123"
}
```

---

#### 3. Verify Hash
```http
GET /verify/{dataset_hash}
```

**Response:**
```json
{
  "dataset_hash": "e3b0c442...",
  "exists_on_chain": true,
  "timestamp": 1738851000,
  "verified_at": "2026-02-06T14:30:00Z"
}
```

---

#### 4. Get User History
```http
GET /history/{user_id}
```

**Response:**
```json
{
  "user_id": "user123",
  "total_datasets": 5,
  "datasets": [
    {
      "id": "abc123",
      "original_filename": "sales_data.csv",
      "dataset_hash": "e3b0c442...",
      "rows_original": 1000,
      "rows_cleaned": 950,
      "created_at": "2026-02-06T14:00:00Z",
      "committed_to_solana": true
    }
  ]
}
```

---

#### 5. Download Cleaned Dataset
```http
GET /download/{dataset_id}
```

Returns the cleaned CSV file for download.

---

## 🧪 Testing

### Running Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Manual Testing

1. **Test Upload Endpoint:**
```bash
curl -X POST "http://localhost:8000/upload?user_id=test123" \
  -F "file=@sample.csv"
```

2. **Test Health Endpoint:**
```bash
curl http://localhost:8000/health
```

3. **Test Verification:**
```bash
curl http://localhost:8000/verify/{hash}
```

### Frontend Testing

```bash
npm test
```

---

## 🖼️ Project Gallery (Screenshots)

<div align="center">

<table>
<tr>
<td align="center">
<img src="public/home1.png" alt="Home 1" width="250px"/><br>
<b>Home 1</b><br>Main homepage interface
</td>
<td align="center">
<img src="public/home2.png" alt="Home 2" width="250px"/><br>
<b>Home 2</b><br>Secondary homepage view / dashboard
</td>
</tr>
<tr>
<td align="center">
<img src="public/upload.png" alt="Upload Page" width="250px"/><br>
<b>Upload Page</b><br>File upload interface for CSV/PDF datasets
</td>
<td align="center">
<img src="public/verify.png" alt="Verification Page" width="250px"/><br>
<b>Verification Page</b><br>Verifying dataset authenticity via `/verify/{hash}`
</td>
</tr>
<tr>
<td align="center">
<img src="public/history.png" alt="History Page" width="250px"/><br>
<b>History Page</b><br>Dashboard showing cleaned datasets and integrity history
</td>
<td align="center">
<img src="public/terminal.png" alt="Terminal" width="250px"/><br>
<b>Terminal</b><br>Local setup / backend running view
</td>
</tr>
</table>

</div>




## 🎥 Short Demo (Compressed)

A short video demo showing the full process — from dataset upload to blockchain verification.

**Demo file:** `assets/keginator-demo.mp4`  


[▶️ Watch demo (1 min)](https://youtu.be/your-demo-link)


---

## 🚀 Deployment Notes

### Backend Deployment (Render)

The backend is hosted on **Render**. Initial load may take a few seconds due to cold start.

**Deployment Steps:**
1. Connect your GitHub repository to Render
2. Configure environment variables in Render dashboard
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel/Netlify)

**Vercel Deployment:**
```bash
npm install -g vercel
vercel deploy
```

**Environment Variables:**
- `NEXT_PUBLIC_API_URL`: Your backend API URL

### Important Security Notes

- ⚠️ Never commit your `SOLANA_PRIVATE_KEY` or API credentials to GitHub
- ⚠️ Keep your `.env` file in `.gitignore`
- ⚠️ Use different keys for development and production
- ⚠️ Enable SSL for all production endpoints
- ⚠️ Ensure your `KEGINATOR_PROGRAM_ID` matches the on-chain program

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: ModuleNotFoundError when starting backend
**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: "GEMINI_API_KEY not set" warning
**Solution:**
- Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Add to `backend/.env`:
```bash
GEMINI_API_KEY=your_key_here
```

#### Issue: Database connection failed
**Solution:**
- The app automatically falls back to SQLite if PostgreSQL is unavailable
- For PostgreSQL: Check `DATABASE_URL` in `.env`
- For local PostgreSQL:
```bash
# Install PostgreSQL
sudo apt-get install postgresql

# Create database
sudo -u postgres createdb keginator
sudo -u postgres createuser keginator -P
```

#### Issue: Solana commitment fails
**Solution:**
- Check `SOLANA_PRIVATE_KEY` is correctly base58 encoded
- Verify Solana devnet is accessible
- Ensure you have SOL balance for gas fees:
```bash
solana balance --url devnet
solana airdrop 1 --url devnet  # Get test SOL
```

#### Issue: Frontend cannot connect to backend
**Solution:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in `backend/app/main.py`
- Ensure `FRONTEND_URL` in `.env` is correct

#### Issue: Audio transcription fails
**Solution:**
- Ensure `faster-whisper` and `av` are installed
- Check `WHISPER_DEVICE` setting (try `cpu` if GPU fails)
- Verify audio file format is MP3 or WAV

### Getting Help

- 📖 Check the [API Documentation](#-api-documentation)
- 🐛 [Open an issue](https://github.com/JaimeCabary/The-keginator/issues)
- 💬 Contact: [@JaimeCabary](https://github.com/JaimeCabary)

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/The-keginator.git
cd The-keginator
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
- Write clean, documented code
- Follow existing code style
- Add tests for new features
- Update README if needed

4. **Test your changes**
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
npm test
```

5. **Commit and push**
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

6. **Create a Pull Request**
- Describe your changes clearly
- Reference any related issues
- Wait for code review

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript**: Follow Airbnb style guide
- **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/)

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features (e.g., more file formats, advanced cleaning algorithms)
- 📝 Documentation improvements
- 🧪 Additional tests
- 🎨 UI/UX enhancements
- 🌍 Internationalization

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] AI-powered data cleaning with Gemini
- [x] Solana blockchain integration
- [x] PostgreSQL metadata storage
- [x] CSV, JSON, XLSX support
- [x] Audio transcription (MP3/WAV)
- [x] Google OAuth authentication
- [x] React frontend with TypeScript

### Phase 2: Enhanced Features 🚧
- [ ] Real-time collaborative cleaning
- [ ] Advanced data visualization
- [ ] Custom cleaning rules engine
- [ ] Batch processing for multiple files
- [ ] API rate limiting and quotas
- [ ] Premium features (Pro/Enterprise plans)

### Phase 3: Ecosystem Expansion 🔮
- [ ] Solana mainnet deployment
- [ ] CLI tool for developers
- [ ] Python SDK for data scientists
- [ ] Integration with Jupyter notebooks
- [ ] Webhook support for automation
- [ ] Data marketplace for verified datasets

### Phase 4: AI Evolution 🤖
- [ ] Support for GPT-4 and Claude
- [ ] Custom AI model training
- [ ] Anomaly detection
- [ ] Predictive data quality scoring
- [ ] Automated data pipeline suggestions

---

## 🛡️ Security & Best Practices

### Security Measures

1. **API Keys**: Never commit credentials to version control
2. **File Validation**: Server-side validation for all uploads
3. **SSL/TLS**: Use HTTPS for all production endpoints
4. **Input Sanitization**: Prevent SQL injection and XSS attacks
5. **Rate Limiting**: Prevent abuse with request throttling
6. **Authentication**: JWT tokens with expiration
7. **CORS**: Whitelist only trusted domains

### Best Practices

- ✅ Validate all uploads on the server (accept only `.csv`, `.json`, `.xlsx`, `.mp3`, `.wav`)
- ✅ Use environment variables for all sensitive configuration
- ✅ Keep dependencies up to date (`pip list --outdated`)
- ✅ Enable debug mode only in development
- ✅ Use proper logging levels (INFO, WARNING, ERROR)
- ✅ Implement request timeouts for external APIs
- ✅ Regular security audits and dependency scanning

---

## 📋 API Endpoints Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | API information and version |
| `/health` | GET | Health check endpoint |
| `/upload` | POST | Upload and clean dataset (CSV/JSON/XLSX/Audio) |
| `/download/{dataset_id}` | GET | Download cleaned dataset |
| `/verify/{hash}` | GET | Verify dataset hash integrity on Solana |
| `/history/{user_id}` | GET | Retrieve user's dataset history |
| `/commit` | POST | Manually commit dataset hash to Solana |
| `/auth/signup` | POST | Create new user account |
| `/auth/login` | POST | User login with email/password |
| `/auth/google` | GET | Google OAuth login redirect |
| `/auth/google/callback` | GET | Google OAuth callback handler |

---

## 🛡️ License

This project is released under the **MIT License**.  
You’re free to use, modify, and build upon it — attribution appreciated.

---

## ❤️ Acknowledgments

Built with ❤️ by **Shalom Chidi-Azuwike**.  

Inspired by sleepless hackathons, dataset chaos, and the drive to make AI infrastructure better for everyone.

> “Half caffeine, half curiosity, 100% unresolved merge conflicts.”  
> — The Keginator Team
