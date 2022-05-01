"""
Python Code To Speech: Reads python code aloud

- Text to speech support from https://pythonbasics.org/text-to-speech/
- Python ast support from https://docs.python.org/3/library/ast.html
"""
import os
import subprocess
import click
from gtts import gTTS

def execute_unix(inputcommand):
    """
    Execute a command and fail
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
        os.system("mpg123 " + file)
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

@click.group()
def python_code_to_speech():
    """
    Group of subcommands
    """

@python_code_to_speech.command()
def gtts():
    '''Command on python_code_to_speech'''
    text = "escape with plane"
    read_text_aloud(text, strategy="gtts")

@python_code_to_speech.command()
def espeak():
    '''Command on python_code_to_speech'''
    text = "Say something in natural language."
    read_text_aloud(text, strategy="espeak")


if __name__ == '__main__':
    python_code_to_speech()
