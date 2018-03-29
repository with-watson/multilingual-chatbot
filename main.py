# lib
import argparse

# src
from src.conversation import Conversation


# main
def main():
    print( 'Initializing bot...' )
    args = parseArguments()
    c = Conversation(
        host=args['host'],
        namespace=args['namespace'],
        package=args['package'],
        action=args['action']
    )
    while True:
        c.converse()


def parseArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument( '--host', help='Host URL for IBM cloud functions',
                         default='openwhisk.ng.bluemix.net' )
    parser.add_argument( '--namespace', help='Namespace for IBM cloud functions',
                         default=None )
    parser.add_argument( '--package', help='Name of package for this action',
                         default='default' )
    parser.add_argument( '--action', help='Name of action deployed as IBM cloud function',
                         default='translator' )

    args = vars( parser.parse_args() )

    # validate
    if args['namespace'] is None:
        parser.error( 'Namespace is required.' )

    return args


if __name__ == '__main__':
    main()
