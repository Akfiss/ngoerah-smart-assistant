"""
Intent Service - Intent classification using LLM
Classifies user messages into intent categories
"""

import json
import logging
import re
from typing import Optional
from dataclasses import dataclass

from app.services.llm_service import LLMService, get_llm_service

logger = logging.getLogger(__name__)


@dataclass
class IntentResult:
    """Result from intent classification"""
    intent: str
    confidence: float
    reasoning: str
    sub_intent: Optional[str] = None


class IntentClassifier:
    """Service for classifying user message intents"""
    
    # Available intents
    INTENTS = {
        'FAQ_QUERY': 'User asking for information',
        'REGISTRATION': 'User wants to register/book appointment',
        'EMERGENCY': 'Urgent medical situation',
        'COMPLAINT': 'User has a complaint',
        'CHITCHAT': 'Casual conversation/greeting'
    }
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm = llm_service or get_llm_service()
        logger.info("Intent Classifier initialized")
    
    def classify(self, user_message: str) -> IntentResult:
        """
        Classify the intent of a user message.
        
        Args:
            user_message: The user's message
            
        Returns:
            IntentResult with intent, confidence, and reasoning
        """
        # First, try quick keyword-based classification for obvious cases
        quick_result = self._quick_classify(user_message)
        if quick_result and quick_result.confidence >= 0.9:
            return quick_result
        
        # Use LLM for nuanced classification
        return self._llm_classify(user_message)
    
    def _quick_classify(self, message: str) -> Optional[IntentResult]:
        """Quick keyword-based classification for common patterns"""
        message_lower = message.lower().strip()
        
        # Greetings
        greetings = ['halo', 'hai', 'hi', 'hello', 'selamat pagi', 'selamat siang', 
                     'selamat sore', 'selamat malam', 'hei', 'hey']
        if message_lower in greetings or any(message_lower.startswith(g) for g in greetings if len(g) > 2):
            return IntentResult(
                intent='CHITCHAT',
                confidence=0.95,
                reasoning='Detected greeting pattern'
            )
        
        # Emergency keywords
        emergency_words = ['darurat', 'emergency', 'gawat', 'kritis', 'sekarat', 
                          'tidak sadar', 'pingsan', 'kecelakaan']
        if any(w in message_lower for w in emergency_words):
            return IntentResult(
                intent='EMERGENCY',
                confidence=0.95,
                reasoning='Detected emergency keywords'
            )
        
        # Registration keywords
        registration_words = ['daftar', 'booking', 'registrasi', 'buat janji', 
                             'jadwal periksa', 'mau periksa']
        if any(w in message_lower for w in registration_words):
            return IntentResult(
                intent='REGISTRATION',
                confidence=0.9,
                reasoning='Detected registration intent'
            )
        
        # Complaint keywords
        complaint_words = ['komplain', 'keluhan', 'kecewa', 'marah', 'protes', 
                          'tidak puas', 'mengecewakan']
        if any(w in message_lower for w in complaint_words):
            return IntentResult(
                intent='COMPLAINT',
                confidence=0.9,
                reasoning='Detected complaint keywords'
            )
        
        return None
    
    def _llm_classify(self, user_message: str) -> IntentResult:
        """Use LLM for detailed intent classification"""
        prompt = f"""Kamu adalah classifier intent untuk chatbot rumah sakit. Analisis pesan pengguna dan klasifikasikan intent-nya.

Pesan Pengguna: "{user_message}"

Intent yang tersedia:
1. FAQ_QUERY - Pengguna bertanya informasi (jadwal, lokasi, biaya, prosedur, jam besuk, dll)
2. REGISTRATION - Pengguna mau daftar/booking/membuat janji dengan dokter
3. EMERGENCY - Situasi medis darurat
4. COMPLAINT - Pengguna komplain atau tidak puas
5. CHITCHAT - Percakapan biasa, sapaan, atau basa-basi

Jawab HANYA dalam format JSON seperti ini (tanpa markdown code block):
{{"intent": "FAQ_QUERY", "confidence": 0.95, "reasoning": "penjelasan singkat"}}

JSON Response:"""

        try:
            response = self.llm.generate(prompt, max_tokens=150, temperature=0.1)
            
            # Parse JSON from response
            result = self._parse_json_response(response)
            
            return IntentResult(
                intent=result.get('intent', 'FAQ_QUERY'),
                confidence=float(result.get('confidence', 0.5)),
                reasoning=result.get('reasoning', 'LLM classification')
            )
            
        except Exception as e:
            logger.error(f"LLM intent classification error: {str(e)}")
            # Default to FAQ_QUERY on error
            return IntentResult(
                intent='FAQ_QUERY',
                confidence=0.5,
                reasoning=f'Fallback due to error: {str(e)}'
            )
    
    def _parse_json_response(self, response: str) -> dict:
        """Parse JSON from LLM response, handling various formats"""
        # Clean the response
        response = response.strip()
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
        if json_match:
            response = json_match.group(1)
        
        # Try to find JSON object
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # Try direct parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Could not parse LLM response as JSON: {response[:100]}")
            return {'intent': 'FAQ_QUERY', 'confidence': 0.5, 'reasoning': 'Parse error'}


# Singleton instance
_intent_classifier: Optional[IntentClassifier] = None


def get_intent_classifier() -> IntentClassifier:
    """Get or create intent classifier singleton"""
    global _intent_classifier
    if _intent_classifier is None:
        _intent_classifier = IntentClassifier()
    return _intent_classifier
