"""
Code To Do Text To Speech

Text to speech support, implemented from: https://pythonbasics.org/text-to-speech/
"""
import os
import subprocess
from gtts import gTTS

def execute_unix(inputcommand):
    """
    Execute an external command and return the output.
    """
    with subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True) as process:
        (output, _stderr) = process.communicate()
        return output

def read_text_aloud(text, strategy="gtts"):
    """
    Read text aloud using the given strategy.

    Assumes that a valid strategy is passed in and throws an exception otherwise.
    """
    if strategy == "gtts":
        file = "file.mp3"

        # initialize tts, create mp3 and play
        tts = gTTS(text, 'com')
        tts.save(file)
        os.system("mpg123 -q " + file)
        os.remove(file)
    elif strategy == "espeak":
        # create wav file
        # w = 'espeak -w temp.wav "%s" 2>>/dev/null' % text
        # execute_unix(w)

        # tts using espeak
        command = f'espeak -ven+f3 -k5 -s150 --punct="<characters>" "{text}" 2>>/dev/null'
        execute_unix(command)
    else:
        raise Exception(f"Unrecognized strategy {strategy}")
