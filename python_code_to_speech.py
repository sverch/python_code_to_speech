"""
Python Code To Speech: Reads python code aloud

- Text to speech support from https://pythonbasics.org/text-to-speech/
- Python ast support from https://docs.python.org/3/library/ast.html
"""
import os
import subprocess
import ast
from num2words import num2words
import click
from gtts import gTTS

TEXT_TO_SPEECH_METHODS = ['gtts', 'espeak']

### Code To Do Text To Speech ###
# Text to speech support, implemented from: https://pythonbasics.org/text-to-speech/

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

### Code To Parse Python Code ###
# Uses this python library that reads the text and gives us a structured "Abstract Syntax Tree"
# representing our python program: https://docs.python.org/3/library/ast.html

# This code all copied from
# https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor

class MyVisitor(ast.NodeVisitor):
    """
    Custom visitor to walk the Abstract Syntax Tree that represents the parsed version of our python
    code and generate a human comprehensible text string.
    """
    def __init__(self, *args, **kwargs):
        self.code_description = ""
        super().__init__(*args, **kwargs)

    def visit(self, node):
        ast.NodeVisitor.visit(self, node)
        return self.code_description

    def generic_visit(self, node):
        # print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    # pylint: disable=invalid-name, missing-function-docstring
    def visit_Call(self, node):

        # See documentation of https://docs.python.org/3/library/ast.html#ast.Call to figure out
        # what properties this has.
        line_number = node.lineno
        name = node.func.id
        arguments = node.args
        number_of_arguments = len(arguments)
        number_of_arguments_string = num2words(number_of_arguments)
        arguments_string = "arguments" if number_of_arguments > 1 else "argument"

        # Add a description of this function to our output.
        self.code_description += (
            f"At line {line_number} we are calling a function named "
            f"\"{name}\" with "
            f"{number_of_arguments_string} {arguments_string}.\n"
        )

        # Now lets add a description of the arguments.
        for (index, argument) in enumerate(arguments):

            # Indexes start at zero, but we don't want to say "zeroeth" for the first argument.
            whichth = num2words(index + 1, to="ordinal")

            if isinstance(argument, ast.Constant):
                self.code_description += (
                        f"The {whichth} argument to {name} is a {type(argument).__name__}, "
                        f"with a type of {type(argument.value).__name__} "
                        f"and a value of {argument.value}\n"
                    )
            else:
                self.code_description += (
                        f"The {whichth} argument to {name} is a {type(argument).__name__}, "
                        "which is something I don't recognize yet\n"
                    )
                continue

        ast.NodeVisitor.generic_visit(self, node)

def python_code_to_text_description(python_code):
    """
    Takes as input text representing some python code and returns text describing that code.
    """
    parsed_python_code = ast.parse(python_code)

    # This will dump out the structure, nice for debugging
    # print(ast.dump(parsed_python_code, indent=4))

    visitor = MyVisitor()

    python_code_description = visitor.visit(parsed_python_code)
    return python_code_description


@click.command(context_settings={'show_default': True})
@click.argument('filename')
@click.option('--text-to-speech-method', type=click.Choice(TEXT_TO_SPEECH_METHODS), default="gtts")
def python_code_to_speech(filename, text_to_speech_method):
    """
    Main command implementation
    """
    with open(filename, "r", encoding="utf8") as file_to_read:
        python_code_lines = file_to_read.readlines()
        python_code = "".join(python_code_lines)

        # Add line numbers to what we print, and also add one because python indexes start at zero
        python_code_with_line_numbers = "".join([
            f"{line_number + 1}: {code_line}"
            for (line_number, code_line) in enumerate(python_code_lines)
            ])

        # Print what we are describing
        print("Describing Python Code:\n")
        print(python_code_with_line_numbers)
        print("\n")

        # Get the text description of our code
        text_description = python_code_to_text_description(python_code)

        # Read the code aloud using the selected method
        if text_to_speech_method == "gtts":
            read_text_aloud(text_description, strategy="gtts")
        elif text_to_speech_method == "espeak":
            read_text_aloud(text_description, strategy="espeak")


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    python_code_to_speech()
