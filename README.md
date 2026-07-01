# PRIVOX - Text Analysis + Amazon Polly TTS

## Overview

Web application that analyzes text for sentiment, PII detection, and converts text to speech using Amazon Polly.

## Features

- ✅ Text sentiment analysis (Positive/Negative/Neutral)
- ✅ PII detection (Email, Phone numbers)
- ✅ Keyword extraction
- ✅ Text-to-speech using Amazon Polly
- ✅ Modern dark UI with animations
- ✅ PII redaction before audio generation (privacy-first)

## Technologies

- **Backend:** Flask, Python
- **AWS Services:** Amazon Comprehend, Amazon Polly
- **Frontend:** HTML5, CSS3, JavaScript
- **SDK:** Boto3 (AWS Python SDK)

## Project Structure

```
PRIVOX-Text-Analysis-Amazon-Polly-TTS/
├── app.py              # Flask backend
├── nlp_utils.py        # NLP analysis functions
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- AWS Account with Comprehend and Polly access
- pip (Python package manager)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/ruchi-raj-shah/PRIVOX-Text-Analysis-Amazon-Polly-TTS-.git
cd PRIVOX-Text-Analysis-Amazon-Polly-TTS-
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure AWS Credentials**

Option A: Using AWS CLI
```bash
aws configure
```

Option B: Using environment variables
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

4. **Run the application**

```bash
python app.py
```

5. **Open in browser**

```
http://localhost:8080
```

## How to Use

1. **Enter Text:** Type or paste text in the textarea
2. **Select Voice:** Choose between female (Joanna) or male (Matthew)
3. **Click "Analyze & Speak"** - Wait for analysis
4. **View Results:**
   - **Sentiment:** Positive, Negative, or Neutral
   - **PII:** Detected personal information types
   - **Keywords:** Top 5 keywords/phrases
   - **Redacted:** Text with PII replaced
   - **Audio:** Listen to Polly TTS reading redacted text

## How It Works

### Architecture

```
Frontend (index.html)
    ↓
    ├── User enters text
    ├── Selects voice
    └── Clicks "Analyze & Speak"
         ↓
    Backend (Flask - app.py)
         ↓
         ├── Receives text via POST
         ├── Calls nlp_utils.analyze_text()
         └── Calls Amazon Polly for TTS
              ↓
         ├── Amazon Comprehend
         │   ├── Sentiment analysis
         │   ├── Keyword extraction
         │   └── PII detection
         │
         └── Amazon Polly
             └── Text-to-Speech (redacted text)
              ↓
    Returns JSON Response
    (sentiment, PII, keywords, redacted, audio)
         ↓
    Frontend displays results
```

### Step-by-Step Process

1. **User Input:** Text submitted via HTML form
2. **Backend Processing:**
   - `app.py` receives POST request
   - Calls `analyze_text(text)` from `nlp_utils.py`
3. **NLP Analysis:**
   - **Sentiment:** Detects positive/negative/neutral
   - **PII:** Finds emails, phone numbers
   - **Keywords:** Extracts top 5 key phrases
   - **Redaction:** Replaces PII with placeholders
4. **Text-to-Speech:**
   - Amazon Polly converts **redacted text** to speech
   - (No raw PII sent to TTS service)
   - Returns MP3 audio as Base64
5. **Frontend Display:**
   - Shows all results with audio player

## API Endpoints

### POST /analyze

**Request:**
```json
{
  "text": "Your text here with contact info",
  "voice": "Joanna"
}
```

**Response:**
```json
{
  "sentiment": "Positive",
  "pii": [
    {
      "type": "EMAIL",
      "values": ["user@example.com"]
    }
  ],
  "keywords": ["word1", "word2", "word3"],
  "redacted": "Your text here with [EMAIL_REDACTED]",
  "audio_b64": "base64_encoded_mp3_audio",
  "voice": "Joanna"
}
```

## AWS Services Used

### Amazon Comprehend

- Detects sentiment (Positive/Negative/Neutral)
- Extracts key phrases (keywords)
- Detects PII entities (email, phone, etc.)
- Supports multiple languages

### Amazon Polly

- Converts text to natural-sounding speech
- Multiple voices available
- Neural voice engine for quality
- MP3 output format

## Security Features

✅ **PII Protection:**
- Detects personal information
- Redacts before TTS (no raw PII in audio)
- Privacy-first approach

✅ **No Credential Exposure:**
- AWS credentials via boto3
- Environment variable based
- No hardcoded secrets

✅ **Input Validation:**
- Text length limit (3000 chars)
- Missing field validation
- Error handling

✅ **CORS Enabled:**
- Frontend-backend communication safe
- Proper error responses

## Course Information

- **Course:** AIGC-5003 - Machine Learning Cloud Computing
- **Institution:** Humber Polytechnic
- **Team:**
  - Ruchi Shah (Student ID: N10020731)
  - Isha Shah

## Learning Outcomes

By building this project, we learned:

✅ **AWS Services**
- Amazon Comprehend for NLP
- Amazon Polly for TTS
- Boto3 SDK for Python

✅ **Full-Stack Development**
- Flask backend architecture
- Frontend-backend communication
- REST API design

✅ **Security Best Practices**
- Credential management
- PII detection and redaction
- Input validation

✅ **NLP Concepts**
- Sentiment analysis
- Keyword extraction
- Entity recognition

✅ **Web Technologies**
- HTML5/CSS3
- JavaScript async/await
- JSON data formats

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

### "Unable to locate credentials"

**Solution:** Configure AWS credentials using one of the methods above

### "Text too long" error

**Solution:** Limit input to 3000 characters

### No audio generated

**Solution:** Check AWS account has Polly access in us-east-1 region

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Custom voice selection
- [ ] Audio file download
- [ ] Translation support
- [ ] Batch processing
- [ ] User authentication
- [ ] Results storage/history
- [ ] Analytics dashboard

## License

MIT License - Free to use and modify

## Contact

For questions or feedback:
- Ruchi Shah
- Isha Shah

---

**Project Status:** ✅ Complete  
**Last Updated:** July 2026  
**Version:** 1.0
