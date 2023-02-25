from __future__ import print_function
import argparse

import yaml
from recognition import AudioInput
from future.builtins.misc import input


parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
                    help="A name of something.")


def get_arguments():
    description = (
        'Flashcards is a small command line tool used to study.\n'
        'Shuffles the content for you and displays the title, once you think\n'
        'you know the answer, by pressing [Enter] you can see the content.\n\n'
        'Expected YML format (keywords are optional):\n\n'
        '-\n'
        '  topic: Python\n'
        '  content: Is a widely used high-level programming language for\n'
        '           created by Guido van Rossum and first released in 1991.\n'
        '  keywords: programming, language\n'
        '-\n'
        '  topic: Javascript\n'
        '  content: Is a dynamic, untyped, and interpreted programming lang.\n')

    formater = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog='flashcards', description=description,
                                     formatter_class=formater)
    parser.add_argument('file_names', metavar='FILE_NAME', nargs='+',
                        help='YML file with flashcards content')
    parser.add_argument('-W', '--writing', action="store_true", default=False,
                        help='answer by writing')
    parser.add_argument('-S', '--speaking', action="store_true", default=False,
                        help='answer by speaking')
    return parser.parse_args()


def generate(args):
    file_name = args.file_names[0]
    writing = args.writing
    speaking = args.speaking
    flashcards = []
    ai = AudioInput()
    continued = True
    try:
        while continued:
            topic = ""
            content = ""

            topic = input("Please input topic) ")
            if speaking:
                content = ai.run()
            else:
                content = input("( ´ゝ`) Write ...)")
            print(f"topic: {topic}")
            print(f"content: {content}")
            flashcards.append({"topic": topic, "content": content})
            a = input(
                "Please [Enter] to proceed, otherwise input some charactors")
            if a == "":
                pass
            else:
                continued = False

        if writing or speaking:
            with open("./yaml/" + file_name, "w", encoding="utf-8") as yf:
                yaml.dump(flashcards, yf, default_flow_style=False,
                          encoding='utf-8', allow_unicode=True)
        else:
            raise Exception("Specify writing or speaking flag")
    except:
        print('Error')
        with open("./yaml/" + file_name, "w", encoding="utf-8") as yf:
            yaml.dump(flashcards, yf, default_flow_style=False,
                      encoding='utf-8', allow_unicode=True)


def main():
    args = get_arguments()
    generate(args)


if __name__ == "__main__":
    main()
