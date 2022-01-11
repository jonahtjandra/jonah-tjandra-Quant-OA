# Documentation

### How to run the script?

First and foremost, pip install the dependencies of the program by using this command: "python -m pip install -r requirements.txt"

The entry point to run the script is the main.py file. In order to run the script properly, main.py will need 2 system arguments: source_data and template. In order to feed this in, use short ops: -t and -d for template and source_data respectively or use long ops --template --source_data. E.g: python main.py -t [template path] -d [source data path]

- Input: Template needs to specify the subject of the email by writing "subject:" as the first word of a line which signifies that line be the subject of the email. The template also needs to include open and close patterns with their keywords enclosed inside these patterns. These keywords will be matched with the source data. All source data needs to include "to", "cc", and "bcc" columns as they will be used in completing the JSON format. Only the "cc" and "bcc" columns are allowed to contain null or empty values.

- Output: In order for the output to preserve the spacing of the email template, the json body output will contain a list of lines.

### Code Structure

The program primarly lives in the email_filler.py. This is the only module you will need to import (assuming dependencies are fullfilled) when using this program in another codebase. The main.py just serves as a driver script for the email_filler.py. email_filler.py is a class that stores information about parsing data into email templates. This is done to allow developers to access insightful information about parsing processes, especially with source_data that have very large sizes. In the src directory we also have 3 important sub-directories: result, test, and sample_data. Result is where the test results are stored and test is the unit testing and sample_data is the data used for testing this program.

### Dealing with patterns and custom patterns

- Default patterns are set to an open pattern: \_\_[ and a close pattern: ]\_\_.

- Pattern customization requires user to provide both an open and close pattern.

- Open and close patterns each needs to have 5 or less characters.

- Tolerance is set to 1 for warnings.

- Dealing with warnings, to notify user that the template might have an incorrectly written pattern by using an assumed tolerance of one character. If a pattern set is found on the template with a single charcter tolerance missing on either the open or close pattern, the program will flag this as a warning and notify the user.

### Sanity Checks and Edge Cases Considered:

- Make sure the email_filler object is created with a template in either a .md extension or .txt extension. Other formats can easily be supported in the future, but in order to ensure our program runs as expected, we need to handle these specific cases.

- The source data in which we use to stub out the fillers are supposed to be given in a CSV format. We handle this by raising an error if it's otherwise.

- Ensure the source data has all the necessary patterns in the template file by raising an exception if this is not fullfilled. Raise a warning log if the source data has more columns than the required patterns in teh template which might indicate that the template is missing some patterns. This assumption holds as we consider the template to have priority over the source data as we need to completely fill the template thus giving only a warning if the template does not use all the source data but raising an error and stopping the program if the source data could not fill in all the patterns in the template. This check is done before running the parse/fill method.

- Handle Case Sensitivity in the pattern and columns from both template and source data by comparing them all in lower case.

- Make sure that the "to" and pattern column does not have a null value in the source_data as we need a recepient for the email.

- The cc and bcc columns are allowed to contain null values.

- Make sure to check that the csv file is in the correct format

- Make sure program is able to handle multiple patterns in one line

### Libraries used

In order to NOT reinvent the wheel and become more efficient, I relied on stable and trusted libraries. I have decided to utilize the following libraries:

- Regex

- Pandas

### Python Style Guide:

- For styling the code base, I chose to adhere to the Google Style Guide (https://google.github.io/styleguide/pyguide.html) and I use yapf linting tool for Python that quickly transforms your code to an easily readable code base, loved by many developers and used by many teams at Google.
