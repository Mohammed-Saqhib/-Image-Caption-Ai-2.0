import pyttsx3
import threading
import sys
import subprocess
import os

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.lock = threading.Lock()
        self.is_mac = sys.platform == 'darwin'
        self.current_voice_id = None  # Store voice ID internally
        self.current_rate = 200  # Store rate internally

    def get_voices(self):
        """
        Get a list of available voices.
        :return: List of voice objects
        """
        return self.engine.getProperty('voices')

    def set_voice(self, voice_id):
        """
        Set the voice for speech synthesis.
        :param voice_id: ID of the voice to use
        """
        self.current_voice_id = voice_id  # Store internally
        self.engine.setProperty('voice', voice_id)

    def set_rate(self, rate):
        """
        Set the speech rate.
        :param rate: Speech rate (default is usually around 200)
        """
        self.current_rate = rate  # Store internally
        self.engine.setProperty('rate', rate)

    def speak(self, text):
        """
        Speak the given text.
        :param text: Text to speak
        """
        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()

    def save_to_file(self, text, filename):
        """
        Save the speech to a file.
        :param text: Text to speak
        :param filename: Output filename (e.g., 'output.wav')
        """
        with self.lock:
            if self.is_mac:
                self._save_to_file_mac(text, filename)
            else:
                self.engine.save_to_file(text, filename)
                self.engine.runAndWait()

    def _save_to_file_mac(self, text, filename):
        """
        Workaround for macOS using 'say' command.
        """
        try:
            # Use internally stored voice ID
            voice_id = self.current_voice_id
            
            if not voice_id:
                # If no voice set, use first available voice
                voices = self.get_voices()
                if voices:
                    voice_obj = voices[0]
                else:
                    raise Exception("No voices available")
            else:
                voice_obj = self._get_voice_by_id(voice_id)
            
            if not voice_obj:
                raise Exception(f"Voice not found for ID: {voice_id}")
            
            # Get the voice name
            voice_name = voice_obj.name
            
            # Remove any parentheses content from voice name for say command
            if '(' in voice_name:
                voice_name = voice_name.split('(')[0].strip()
            
            # Use internally stored rate
            rate = self.current_rate
            
            # Build say command
            cmd = ['say', '-v', voice_name, '-r', str(rate), '-o', filename, '--data-format=LEF32@22050', text]
            
            # Debug output
            print(f"Running command: say -v '{voice_name}' -r {rate} -o {filename}")
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if not os.path.exists(filename):
                raise Exception(f"Audio file not created: {filename}")
                
        except subprocess.CalledProcessError as e:
            print(f"Error in macOS say command: {e.stderr}")
            raise Exception(f"Failed to generate audio: {e.stderr}")
        except Exception as e:
            print(f"Error in mac save workaround: {e}")
            raise e

    def _get_voice_by_id(self, voice_id):
        """Get voice object by ID"""
        voices = self.get_voices()
        for voice in voices:
            if voice.id == voice_id:
                return voice
        return None


if __name__ == "__main__":
    tts = TTSEngine()
    voices = tts.get_voices()
    for voice in voices:
        print(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")
