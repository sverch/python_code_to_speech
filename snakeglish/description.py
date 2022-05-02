"""
Code To Parse Python Code

Uses this python library that reads the text and gives us a structured "Abstract Syntax Tree"
representing our python program: https://docs.python.org/3/library/ast.html

This code mostly copied from
https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
"""
import ast
from num2words import num2words


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
            f"On line {line_number} we are calling a function named "
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

def code_to_description(code):
    """
    Takes as input text representing some python code and returns text describing that code.
    """
    parsed_python_code = ast.parse(code)

    # This will dump out the structure, nice for debugging
    # print(ast.dump(parsed_python_code, indent=4))

    visitor = MyVisitor()

    python_code_description = visitor.visit(parsed_python_code)
    return python_code_description
