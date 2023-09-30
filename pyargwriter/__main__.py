

from argparse import ArgumentParser

from pyargwriter.utils.parser import setup_parser
from pyargwriter.process import ArgParseWriter

def main():
    parser = ArgumentParser(description="PyArgWriter: Python Argument Parser Setup Writer",
        epilog="Automatically generates ArgumentParser setups for Python classes and their methods.",)
    parser = setup_parser(parser)

    args_dict = vars(parser.parse_args())
    arg_pars_writer = ArgParseWriter(**args_dict)
    if args_dict["command"] == "parse-code":
        arg_pars_writer.parse_code(**args_dict)
    elif args_dict["command"] == "write-code":
        arg_pars_writer.write_code(**args_dict)
    elif args_dict["command"] == "generate-parser":
        arg_pars_writer.generate_parser(**args_dict)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()