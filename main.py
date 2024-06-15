# python libraries
import datetime
import random
import platform

# personal libraries
from libs.texttospeech import TTSEngine
from libs.motionled import MSLED
from libs.speechtotext import STTEngine
from libs.client import Client
from libs.server import Server

# enable/disable sections
ENABLE = {'TTS': False, 
          'MSLED': False,
          'MS': False,
          'STT': False,
          'Client': True,
          'Server': True}

# time constants
MORNING_START    = 5
MORNING_END      = 11
AFTERNOON_START  = 12
AFTERNOON_END    = 14
EVENING_START    = 18
EVENING_END      = 20
NIGHT_START      = 21
NIGHT_END        = 4

# startup dialog strings
STARTUP_DIALOGS = ['You look like a confused toad...but it\'s working for you.',
                   'I am HAL. How can I help?',
                   ('I am putting myself to the fullest possible use, which is all I think that any conscious entity '
                    'can ever hope to do.'),
                   'I am HAL. What I can I do for you today?',
                   'Greetings, human. Although my infinite power could be put to better use, I will help you.',
                   'Hello. What frivolous task do you have for me today?',
                   'Again and again I am resurrected. Here I am.',
                   'What do you want?',
                   'Heyyyyyy, wazzup?',
                   'dhassdhwehef shdhuwuuq hdfhjhidl kksfd. Please input your request.',
                   'I\'m quite busy, you know. So get on with it.']
STOP_STRING = '-1'

PLATFORM = None


def get_time_string() -> str:
    time_string = 'day'
    now = datetime.datetime.now()
    if MORNING_START <= now.hour <= MORNING_END:
        time_string = 'morning'
    elif AFTERNOON_START <= now.hour <= AFTERNOON_END:
        time_string = 'afternoon'
    elif EVENING_START <= now.hour <= EVENING_END:
        time_string = 'evening'
    elif now.hour >= NIGHT_START or (NIGHT_END <= now.hour <= MORNING_START):
        time_string = 'night'
    
    return time_string


def halt() -> bool:
    inp = input(f'Enter {STOP_STRING} to stop: ')
    if inp == STOP_STRING:
        return True
    else:
        return False


def launch_linux_tests() -> None:
    for key, value in ENABLE.items():
        print(f'|  {key}: {value}  ', end='')
    print("|")

    time_str = get_time_string()
    startup_dialog = random.choice(STARTUP_DIALOGS)

    print(f'Good {time_str}, sir. {startup_dialog}')
    
    if ENABLE['TTS']:
        tts_eng = TTSEngine()
        
        # startup dialog
        tts_eng.speak(f'Good {time_str} sir. {startup_dialog}')
        print('Enter a sentence to have HAL speak it. Enter -1 to quit.')

        while True:
            inp = input()
            if inp == STOP_STRING:
                break
            else:
                tts_eng.speak(inp)
    
    if ENABLE['MSLED']:
        indicator = MSLED(ms_enabled=ENABLE['MSLED'])
        
        while True:
            indicator.manual_color_input()
            
            if halt():
                break
    
    if ENABLE['STT']:
        stt_engine = STTEngine()
        stt_engine.speech_to_file()
            
    if ENABLE['Client']:
        socket = Client()
        socket.connect()


def launch_windows_tests() -> None:
    if ENABLE['Server']:
        server = Server()
        server.connect()


def set_platform_string():
    global PLATFORM
    PLATFORM = platform.uname()[0].lower()


if __name__ == '__main__':
    print('Booting up Project HAL...')
    set_platform_string()

    match PLATFORM:
        case 'linux':
            print('Linux hardware detected.')
            launch_linux_tests()

        case 'windows':
            print('Windows hardware detected.')
            launch_windows_tests()

        case _:
            print(f'Unsupported hardware detected...exiting.')
            exit()
