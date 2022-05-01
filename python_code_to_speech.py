import click

@click.group()
def python_code_to_speech():
    pass

@python_code_to_speech.command()
def cmd1():
    '''Command on python_code_to_speech'''
    click.echo('python_code_to_speech cmd1')

@python_code_to_speech.command()
def cmd2():
    '''Command on python_code_to_speech'''
    click.echo('python_code_to_speech cmd2')

if __name__ == '__main__':
    python_code_to_speech()
