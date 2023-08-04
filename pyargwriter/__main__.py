

from argparse import ArgumentParser

from pyargwriter.parser import setup_parser
from pyargwriter.process import ArgParsWriter

def main():
    parser = ArgumentParser(description="PyArgWriter: Python Argument Parser Setup Writer",
        epilog="Automatically generates ArgumentParser setups for Python classes and their methods.",)
    parser = setup_parser(parser)

    args_dict = vars(parser.parse_args())
    arg_pars_writer = ArgParsWriter(**args_dict)
    if args_dict["command"] == "generate-argparser":
        arg_pars_writer.generate_parser()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()