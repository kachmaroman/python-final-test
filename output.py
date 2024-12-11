from gtts import gTTS
from pygame import mixer
import os
import time
import uuid
from contextlib import contextmanager

def get_temp_dir():
    temp_dir = os.path.join(os.path.dirname(__file__), "temp_audio")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    return temp_dir

@contextmanager
def audio_player():
    if not mixer.get_init():
        mixer.init()
    try:
        yield
    finally:
        mixer.music.stop()
        mixer.music.unload()


def cleanup_temp_files():
    temp_dir = get_temp_dir()
    for file in os.listdir(temp_dir):
        try:
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path) and file.endswith('.mp3'):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not remove old file {file}: {str(e)}")


def say(text):
    temp_dir = get_temp_dir()
    filename = os.path.join(temp_dir, f"speech_{uuid.uuid4()}.mp3")

    try:
        # Generate speech file
        tts = gTTS(text, lang='uk')
        with open(filename, 'wb') as f:
            tts.write_to_fp(f)

        # Play audio with proper resource management
        with audio_player():
            mixer.music.load(filename)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Could not remove temp file {filename}: {str(e)}")


#cleanup_temp_files()

test_phrases = [
    "Привіт, як справи?",
    "Як тебе звати?",
    "Мене звати Python!"
]

# for phrase in test_phrases:
#     say(phrase)
#     time.sleep(0.2)