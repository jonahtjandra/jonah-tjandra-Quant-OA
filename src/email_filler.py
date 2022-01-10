import pandas as pd


class EmailFiller:

    # template : string representation of relative path of the template email file
    # csv : string representation of relative path of the source data
    def __init__(self, template: str, source_data: str) -> None:
        if template.lower().endswith(".md") or source_data.lower().endswith(
                ".txt"):
            self.template = template
            self.source_data = source_data
        else:
            raise Exception(
                "Make sure the template and source data is in the right file format according to the documenation"
            )

    def fill_template():
        print("stubbed")
