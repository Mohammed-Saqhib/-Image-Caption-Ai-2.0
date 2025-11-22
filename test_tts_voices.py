#!/usr/bin/env python3
"""Test TTS with different voices"""

import sys
sys.path.append('src')

from tts_engine import TTSEngine

def test_voice_languages():
    print("Testing TTS Engine with different languages...\n")
    
    tts = TTSEngine()
    voices = tts.get_voices()
    
    # Test cases for different languages
    test_languages = {
        'Hindi': 'नमस्ते',
        'Kannada': 'ನಮಸ್ಕಾರ',
        'Tamil': 'வணக்கம்',
        'English': 'Hello'
    }
    
    for voice in voices:
        voice_lang = str(voice.languages[0]) if voice.languages else 'unknown'
        
        # Check for Hindi
        if 'hi_IN' in voice_lang:
            print(f"Testing Hindi voice: {voice.name}")
            tts.set_voice(voice.id)
            tts.set_rate(200)
            tts.save_to_file(test_languages['Hindi'], 'test_hindi.wav')
            print(f"✅ Created test_hindi.wav with voice {voice.name}\n")
            break
    
    # Check for Kannada
    for voice in voices:
        voice_lang = str(voice.languages[0]) if voice.languages else 'unknown'
        if 'kn_IN' in voice_lang:
            print(f"Testing Kannada voice: {voice.name}")
            tts.set_voice(voice.id)
            tts.set_rate(200)
            tts.save_to_file(test_languages['Kannada'], 'test_kannada.wav')
            print(f"✅ Created test_kannada.wav with voice {voice.name}\n")
            break
    
    print("Test complete! Check the generated wav files.")

if __name__ == "__main__":
    test_voice_languages()
