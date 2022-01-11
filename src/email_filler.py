from os import close
import pandas as pd
import json
import logging


class EmailFiller:

    # template: string representation of relative path of the template email file
    # source_data: string representation of relative path of the source data
    # return: None
    def __init__(self,
                 template: str,
                 source_data: str,
                 open_pattern: str = "__[",
                 close_pattern: str = "]__",
                 pattern_tolerance: int = 1) -> None:
        # ensure open and close patterns are each less than or equal to 5 characters long as per documentation
        if not len(open_pattern) <= 5 and len(close_pattern) <= 5:
            raise Exception(
                "Your custom pattern is greater than 4 characters long and is not allowed as per documentation"
            )
        # ensure tolerance is valid as per documentation
        if min(len(open_pattern), len(close_pattern)) >= pattern_tolerance:
            raise Exception(
                "Make sure your tolerance is greater than the minimum length of your pattern"
            )
        # ensure source_data is a csv
        if not source_data.lower().endswith(".csv"):
            raise Exception("Make sure the source data is in csv format")
        # instance variable for storing data source as a pandas dataframe so we can easily manipulate csv files
        try:
            self.source_df = pd.read_csv(source_data)
        except:
            raise Exception("Make sure the source data is in the right format")
        # instance variable for storing parse index used for continuing program where the program last left off
        self.parse_index = 0
        # ensure template is either a md or txt file as per documentation
        if template.lower().endswith(".md") or template.lower().endswith(
                ".txt"):
            self.template = template
            self.source_data = source_data
        else:
            raise Exception(
                "Make sure the template and source data is in the right file format according to the documenation"
            )
        self.open_pattern = open_pattern
        self.close_pattern = close_pattern
        self.pattern_tolerance = pattern_tolerance
        # parse template for column data

        # checks if the template itself might contain any errors

        # ensure the source data has no errors:  null check for source_data columns as per documenation and contains all the neccessary columns for the pattern in the template

    # returns a list of column data
    def parse_template(self) -> list:
        print("stubbed")

    # returns a boolean value whether the template might contain an error
    def is_valid_template(self) -> bool:
        print("stubbed")

    # returns a boolean value whether the source data has errors
    def check_source_data(self) -> bool:
        print("stubbed")

    # output_file: path to where we want to save our result
    # file_name: name of the output file
    # return: status of filling template, returning issues, warnings, or errors
    def fill_template(self, output_file: str, file_name: str) -> str:
        status = {"time elapsed": "", "patterns": [], "warnings": []}
        patterns = []

        result = []
        record = {"to": "", "cc": "", "bcc": "", "subject": [], "body": ""}
        if self.template.lower().endswith(".md"):
            file = open(self.template, "r")
            for line in file:
                print(line)
                if line.isspace():
                    print("This is an empty line")
        elif self.template.lower().endswith(".txt"):
            file = open(self.template, "r")
            for line in file:
                print(line)
                if line.isspace():
                    print("This is an empty line")

    # return: status of filling template, returning issues, warnings, or errors
    def continue_fill(self) -> str:
        print("stubbed")

    # this is to get the latest info on runs
    def get_info(self) -> str:
        return "this is the information about this email filler instance"
