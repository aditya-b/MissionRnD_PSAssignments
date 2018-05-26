import click

def removealldigits(arg):
    for i in range(10):
        arg = arg.replace(ascii(i), '')
    return arg
@click.group()
@click.option('--removedigits / --no-removedigits',default=False,help='remove digits from input')
@click.pass_context
def function_main(context,removedigits):
    '''Supports some string commands from command line'''
    context.obj['remdig']=removedigits

@function_main.command()
@click.option("--delimiter",'-d',default=':',help="Defaults to :")
@click.argument('args',nargs=-1,required=True)
@click.pass_context
def concat(context,delimiter,args):
    '''concatenates passed in strings with delimiter'''
    str=''
    for arg in args:
        if context.obj['remdig']:
            arg=removealldigits(arg)
        str+=arg+delimiter
    str=str[:-1]
    click.echo(str)

@function_main.command()
@click.argument('arg',nargs=1,required=True)
@click.pass_context
def lower(context,arg):
    '''converts the word to lower case'''
    if context.obj['remdig']:
        arg=removealldigits(arg)
    click.echo(arg.lower())

@function_main.command()
@click.argument('arg',nargs=1,required=True)
@click.pass_context
def upper(context,arg):
    '''converts the word to upper case'''
    if context.obj['remdig']:
        arg=removealldigits(arg)
    click.echo(arg.upper())


if __name__=='__main__':
    function_main(obj={})