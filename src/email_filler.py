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
                 open_pattern: str = "__\[",
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
                    raise Exception(
                        f"Columns in the source data except for cc and bcc are not allowed to be null. Column {column} has null values"
                    )

    def check_template(self) -> None:
        template_file = open(self.template, "r")
        keywords_pattern = f"(?<={self.open_pattern})(.+)(?={self.close_pattern})"
        keywords = re.findall(keywords_pattern, template_file.read())
        # check if all keywords in the template exist as a column in source data
        for keyword in keywords:
            if not keyword in self.source_df.columns:
                raise Exception(
                    "Keyword '{keyword}' is not in the source data. Please check that the keywords and columns match."
                )
        # check if all source data columns exist as a pattern in email template
        for column in self.source_df:
            if column == "to" or column == "cc" or column == "bcc":
                continue
            if not column in keywords:
                logging.warning(
                    "There might be a typo for the open and close patterns in the template email. Check both the result and the template email to see if unexpected result exist. If it does, ensure that the custom or default patterns match the template patterns."
                )
                raise Exception(
                    f"Email template does not contain column '{column}' from source data."
                )

        # check variation of keyword patterns with tolerance of 1
        open_pattern = re.sub(r"\\", "", self.open_pattern)
        close_pattern = re.sub(r"\\", "", self.close_pattern)
        for j in range(len(close_pattern)):
            keywords_pattern = f"([,.!\?(\* ])(?<={re.escape(open_pattern)})(.+)(?={re.escape(close_pattern[0:j] + close_pattern[j+1:])})([,.!\?(\* ])"
            if len(re.findall(keywords_pattern, template_file.read())) != 0:
                logging.warning(
                    "There might be a typo for the open and close patterns in the template email. Check both the result and the template email to see if unexpected result exist. If it does, ensure that the custom or default patterns match the template patterns."
                )

        for i in range(len(self.open_pattern)):
            keywords_pattern = f"([,.!\?(\* ])(?<={re.escape(open_pattern[0:i] + open_pattern[i+1:])})(.+)(?={re.escape(close_pattern)})([,.!\?(\* ])"
            if len(re.findall(keywords_pattern, template_file.read())) != 0:
                logging.warning(
                    "There might be a typo for the open and close patterns in the template email. Check both the result and the template email to see if unexpected result exist. If it does, ensure that the custom or default patterns match the template patterns."
                )
        template_file.close()

    # output_file: path to where we want to save our result
    # return: status of filling template, returning issues, warnings, or errors
    def fill_template(self, output_file: str) -> str:
        # check the source data obeys null value rule as per documentation
        self.check_source_data()
        status = {"time elapsed": "", "patterns": [], "warning": []}
        result = []
        regex_pattern = f"{self.open_pattern}.+{self.close_pattern}"
        keywords_pattern = f"(?<={self.open_pattern})(.+)(?={self.close_pattern})"
        for index, row in self.source_df.iterrows():
            logging.info(f"Processing row {index}")
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
                        line_replace = re.sub(
                            f"{self.open_pattern}{keyword}{self.close_pattern}",
                            row[keyword], line_replace)
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
