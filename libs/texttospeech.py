import pyttsx3

# speech constants
HEADING_STR = "uh"
TRAILING_STR = ""
WINDOWS_GEORGE_ID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_GEORGE_11.0"


class TTSEngine:
    def __init__(self, voice_id='english-us'):
        self.engine = pyttsx3.init()  # initializing TTS engine
        self.set_voice(voice_id)

        self.heading_str = HEADING_STR
        self.trailing_str = TRAILING_STR

    def set_voice(self, voice_id: str):
        self.engine.setProperty('voice', voice_id)

    def gather_voice_ids(self):
        voices = self.engine.getProperty('voices')

        for voice in voices:
            print(f'Voice: {voice}')

    def speak(self, string_to_speak: str) -> None:
        self.engine.say(f'{self.heading_str} {string_to_speak} {self.trailing_str}')
        self.engine.runAndWait()
        self.engine.stop()
