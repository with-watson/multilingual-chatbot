# lib
import argparse

# src
from src.conversation import Conversation


# main
def main():
    print( 'Initializing bot...' )
    args = parseArguments()
    c = Conversation( key=args['key'], namespace=args['namespace'] )
    while True:
        c.Converse()


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument( '--key' )
    parser.add_argument( '--namespace' )

    args = vars( parser.parse_args() )

    # validate
    return args


if __name__ == '__main__':
    main()
