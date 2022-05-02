"""
Python Code To Speech: Reads python code aloud
"""
import click
from snakeglish.description import code_to_description
from snakeglish.speak import read_text_aloud
from snakeglish.numberlines import add_line_numbers

TEXT_TO_SPEECH_METHODS = ['gtts', 'espeak']


@click.command(context_settings={'show_default': True})
@click.argument('filename')
@click.option('--text-to-speech-method', type=click.Choice(TEXT_TO_SPEECH_METHODS), default="gtts")
@click.option('--print-only', is_flag=True, help="Print but don't speak.")
def python_code_to_speech(filename, text_to_speech_method, print_only):
    """
    Main command implementation
    """
    with open(filename, "r", encoding="utf8") as file_to_read:
        code = file_to_read.read()

        # Print what we are describing
        print("Describing Python Code:\n")
        print(add_line_numbers(code))
        print("\n")

        # Get the text description of our code
        description = code_to_description(code)
        print(description)

        if not print_only:
            # Read the code aloud using the selected method
            if text_to_speech_method == "gtts":
                read_text_aloud(description, strategy="gtts")
            elif text_to_speech_method == "espeak":
                read_text_aloud(description, strategy="espeak")


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    python_code_to_speech()
