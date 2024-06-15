import vosk
import pyaudio
import json

SAMPLE_RATE = 16000
BUFFER_FRAMES = 8192

FILTER_SOUNDS = ['', ' ', '\n']
MODEL_PATH = 'models/vosk-model-en-us-0.22-lgraph'

class STTEngine:
    def __init__(self) -> None:
        # initialize the model with the path to the right model
        print('Starting up vosk model...')
        self.model = vosk.Model(MODEL_PATH)

        # pass in the model and the sample rate (Hz)
        print('Starting up vosk recognizer...')
        self.rec = vosk.KaldiRecognizer(self.model, SAMPLE_RATE)

        # open the microphone stream
        print('Opening microphone stream...')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=BUFFER_FRAMES)
    
    def __del__(self) -> None:
        # terminate the stream and pyaudio objects
        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()

    def speech_to_file(self, file_path = 'data/recognized_text.txt'):

        with open(file_path, 'w') as file:
            print('Listening for speech. Say \'Terminate\' to stop.')

            # start streaming and recognizing speech
            while True:
                data = self.stream.read(BUFFER_FRAMES)  # read in chunks of 4096 bytes (increase if you get an overflow)
                if self.rec.AcceptWaveform(data):  # accept waveform of input voice
                    # parse the JSON result and get the recognized text
                    result = json.loads(self.rec.Result())
                    recognized_text = result['text']

                    # filter out the non-word sounds
                    if recognized_text in FILTER_SOUNDS:
                        continue

                    # write the speech to the file and print it
                    file.write(recognized_text + '\n')
                    print(recognized_text)

                    # Check for the termination keyword
                    if 'terminate' in recognized_text.lower():
                        print('Termination keyword detected. Stopping...')
                        break
