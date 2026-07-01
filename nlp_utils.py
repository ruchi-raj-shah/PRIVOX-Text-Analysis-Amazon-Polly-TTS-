import re
from collections import Counter
import boto3
 
# Initialize Comprehend client
comprehend_client = boto3.client('comprehend', region_name='us-east-1')  # change region if needed
 
def analyze_text(text, language_code='en'):
    if not text:
        return {'error': 'No text provided'}
 
    # ---- 1. Call Amazon Comprehend ----
    # Sentiment
    sentiment_resp = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode=language_code
    )
    sentiment = sentiment_resp.get('Sentiment', 'NEUTRAL').title()  # e.g. "Positive"
 
    # Key phrases (we’ll treat these as "keywords" for your UI)
    key_phrases_resp = comprehend_client.detect_key_phrases(
        Text=text,
        LanguageCode=language_code
    )
    key_phrases = [kp['Text'] for kp in key_phrases_resp.get('KeyPhrases', [])]
    # Deduplicate while preserving order and limit to 5
    seen = set()
    keywords = []
    for kp in key_phrases:
        if kp.lower() not in seen:
            seen.add(kp.lower())
            keywords.append(kp)
        if len(keywords) >= 5:
            break
 
    # PII entities (standard Comprehend PII API)
    pii = []
    pii_resp = None
    try:
        pii_resp = comprehend_client.detect_pii_entities(
            Text=text,
            LanguageCode=language_code
        )
    except Exception:
        # detect_pii_entities is not available in all regions/accounts
        pii_resp = {'Entities': []}
 
    entities = pii_resp.get('Entities', []) if pii_resp else []
 
    # Convert entities to a simpler structure for your frontend
    pii_values_by_type = {}
    for ent in entities:
        etype = ent.get('Type', 'UNKNOWN')
        start = ent.get('BeginOffset', 0)
        end = ent.get('EndOffset', 0)
        value = text[start:end]
        pii_values_by_type.setdefault(etype, set()).add(value)
 
    for etype, values in pii_values_by_type.items():
        pii.append({
            'type': etype,
            'values': list(values)
        })
 
    # ---- 2. Redact the PII in the original text ----
    redacted = text
    # Sort entities by BeginOffset descending so replacements don’t mess up indices
    for ent in sorted(entities, key=lambda e: e['BeginOffset'], reverse=True):
        start = ent.get('BeginOffset', 0)
        end = ent.get('EndOffset', 0)
        etype = ent.get('Type', 'PII')
        placeholder = f'[{etype}_REDACTED]'
        redacted = redacted[:start] + placeholder + redacted[end:]
 
    # ---- 3. Build the result object (same structure as before) ----
    return {
        'pii': pii,                 # list of {type, values}
        'sentiment': sentiment,     # e.g. "Positive"
        'keywords': keywords,       # top ~5 key phrases
        'redacted': redacted        # PII-redacted text
    }