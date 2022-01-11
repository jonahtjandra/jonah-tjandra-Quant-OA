import pandas as pd
import json


class EmailFiller:

    # template: string representation of relative path of the template email file
    # csv: string representation of relative path of the source data
    # return: None
    def __init__(self, template: str, source_data: str) -> None:
        # ensure source_data is a csv
        if not source_data.lower().endswith(".csv"):
            raise Exception("Make sure the source data is in csv format")
        # instance variable for storing data source as a pandas dataframe so we can easily manipulate csv files
        self.source_df = pd.read_csv(source_data)
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
        # ensure the source data has all the neccessary columns for the pattern in the template

    # output_file: path to where we want to save our result
    # file_name: name of the output file
    # return: status of filling template, returning issues, warnings, or errors
    def fill_template(self, output_file: str, file_name: str) -> str:

        result = []
        source_pd = pd.read_csv(self.source_data)
        record = {"to": "", "cc": "", "bcc": "", "subject": "", "body": ""}
        if self.template.lower().endswith(".md"):
            print("test")
        elif self.template.lower().endswith(".txt"):
            file = open(self.template, "r")
            for line in file:
                for word in line.split():
                    print(word)
