from numpy.lib.utils import source
from email_filler import EmailFiller
import sys, logging, getopt


def main():
    args = sys.argv[1:]
    output_file = "./result/output.json"
    template = ""
    source_data = ""
    if not len(args) == 4:
        raise Exception(
            "Please enter the write number of arguments according to the documentation"
        )
    try:
        arguments, args = getopt.getopt(args, "t:d:",
                                        ["template=", "source_data="])
    except:
        raise Exception(
            "You did not specify email template or source data or both")
    for argument, value in arguments:
        if argument in ["-t", "--template"]:
            template = value
            print(value)
            print("template")
        elif argument in ["-d", "--source_data"]:
            source_data = value
            print(value)
            print("source data")
    parser = EmailFiller(template, source_data)
    parser.fill_template(output_file)


main()