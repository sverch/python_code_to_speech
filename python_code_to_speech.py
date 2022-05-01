"""
Python Code To Speech: Reads python code aloud
"""
import os
import click
from gtts import gTTS

@click.group()
def python_code_to_speech():
    """
    Group of subcommands
    """

@python_code_to_speech.command()
def gtts():
    '''Command on python_code_to_speech'''

    # define variables
    text = "escape with plane"
    file = "file.mp3"

    # initialize tts, create mp3 and play
    tts = gTTS(text, 'com')
    tts.save(file)
    os.system("mpg123 " + file)

@python_code_to_speech.command()
def cmd2():
    '''Command on python_code_to_speech'''
    click.echo('python_code_to_speech cmd2')




if __name__ == '__main__':
    python_code_to_speech()
