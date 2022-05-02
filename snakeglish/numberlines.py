"""
Utility to add line numbers to a block of code, for nice reference when reading out which line does
what.
"""
def add_line_numbers(code):
    """
    Given a code string, output a string with "<lineno>: " prepended to each line.
    """
    return "\n".join([
        f"{line_number + 1}: {code_line}"
        for (line_number, code_line) in enumerate(code.split("\n"))
        ])
