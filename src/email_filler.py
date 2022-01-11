from os import close
import re
from numpy import NaN
from numpy.lib.utils import source
import pandas as pd
import json
import logging


class EmailFiller:
    # logging configuration
    logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
                        level=logging.INFO)

    # template: string representation of relative path of the template email file
    # source_data: string representation of relative path of the source data
    # return: None
    def __init__(self,
                 template: str,
                 source_data: str,
                 open_pattern: str = "_\[",
                 close_pattern: str = "\]__") -> None:
        # ensure open and close patterns are each less than or equal to 5 characters long as per documentation
        if not len(open_pattern) <= 5 and len(close_pattern) <= 5:
            raise Exception(
                "Your custom pattern is greater than 4 characters long and is not allowed as per documentation"
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

        self.check_template()

    def check_source_data(self) -> None:
        for column in self.source_df:
            if column == "cc" or column == "bcc":
                continue
            else:
                if self.source_df[column].isnull().values.any():
                    print(self.source_df[column].values)
                    raise Exception(
                        f"Columns in the source data except for cc and bcc are not allowed to be null. Column {column} has null values"
                    )

    def check_template(self) -> None:
        template_file = open(self.template, "r")
        keywords_pattern = f"(?<={self.open_pattern})(.+)(?={self.close_pattern})"
        keywords = re.findall(keywords_pattern, str(template_file))
        for keyword in keywords:
            if not self.source_df[keyword]:
                raise Exception(
                    "Keyword is not in the source data. Please check that the keywords and columns match."
                )
        # check variation of keyword patterns with tolerance of 1
        for i in range(len(self.open_pattern)):
            for j in range(len(self.close_pattern)):
                keywords_pattern = f"(?<={self.open_pattern[(0 if i != 0 else 1):i] + self.open_pattern[(i if i != 0 else len(self.open_pattern)):]})(.+)(?={self.close_pattern[(0 if i != 0 else 1):i] + self.close_pattern[(i if i != 0 else len(self.close_pattern)):]})"
                try:
                    re.findall(keywords_pattern, str(template_file)).group()
                except:
                    logging.warning(
                        "There might be a typo for the open and close patterns in the template email. Check the both the result and the template email to see if unexpected result exist. If it does, that means a typo occured in the template"
                    )

    # output_file: path to where we want to save our result
    # return: status of filling template, returning issues, warnings, or errors
    def fill_template(self, output_file: str) -> str:
        # check the source data obeys null value rule as per documentation
        self.check_source_data()
        status = {"time elapsed": "", "patterns": [], "warning": []}
        result = []
        regex_pattern = f"{self.open_pattern}.+{self.close_pattern}"
        keywords_pattern = f"(?<={self.open_pattern})(.+)(?={self.close_pattern})"
        print(keywords_pattern)
        for index, row in self.source_df.iterrows():
            logging.info(f"We are processing row {index}")
            record = {
                "to": row["to"],
                "cc": row["cc"] if row["cc"] == NaN else "",
                "bcc": row["bcc"] if row["bcc"] == NaN else "",
                "subject": "test_run_no_subject_yet",
                "body": []
            }
            file = open(self.template, "r")
            for line in file:
                # find patterns
                patterns = re.findall(regex_pattern, str(line))
                keywords = re.findall(keywords_pattern, str(line))
                # check for subject in email template
                if line[0:8].lower() == "subject:":
                    record["subject"] = line[8:]
                    continue
                elif line.isspace():
                    continue
                else:
                    # handling multiple patterns in a line
                    line_replace = line
                    for pattern, keyword in zip(patterns, keywords):
                        print(pattern, row[keyword])
                        line_replace = re.sub(
                            f"{self.open_pattern}{keyword}{self.close_pattern}",
                            row[keyword], line_replace)
                        print(line_replace)
                    record["body"].append(line_replace)
            result.append(record)

        # write result to json file
        json_output = json.dumps(result, indent=2)
        json_file = open(output_file, "w")
        json_file.write(json_output)
        json_file.close()

    # return: status of filling template, returning issues, warnings, or errors
    def continue_fill(self) -> str:
        print("stubbed")

    # this is to get the latest info on runs
    def get_info(self) -> str:
        return "this is the information about this email filler instance"
