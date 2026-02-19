import numpy as np
import sounddevice as sd
import speech_recognition as sr


class VoiceSTT:
    def __init__(self,
                 device="hw:1,0",
                 fs=48000,
                 duration=3.0,
                 lang="th-TH"):
        """
        device   : ALSA device (e.g., "hw:2,0")
        fs       : sample rate (44100 or 48000 for your microphone)
        duration : recording time in seconds
        lang     : language for Google STT
        """
        self.device = device
        self.fs = int(fs)
        self.duration = float(duration)
        self.lang = lang
        self.recognizer = sr.Recognizer()

    def listen(self):
        """
        Record audio -> Send to Google STT -> Return recognized text or None
        """
        try:
            frames = int(self.fs * self.duration)

            print(f"Listening for {self.duration} seconds...")
            audio_raw = sd.rec(frames,
                               samplerate=self.fs,
                               channels=1,
                               dtype="int16",
                               device=self.device,
                               blocking=True)

            data = audio_raw[:, 0]

            # Convert to SpeechRecognition AudioData
            audio = sr.AudioData(data.tobytes(),
                                 sample_rate=self.fs,
                                 sample_width=2)

            print("Recognizing...")
            text = self.recognizer.recognize_google(
                audio,
                language=self.lang
            ).strip()

            return text

        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None

        except sr.RequestError as e:
            print("Google STT error:", e)
            return None

        except Exception as e:
            print("Error:", e)
            return None


# # ---- Example usage ----
# stt = VoiceSTT(lang="en-US")  # Change language here if needed

# while True:
#     result = stt.listen()

#     if result:
#         print("🗣️ You said:", result)
