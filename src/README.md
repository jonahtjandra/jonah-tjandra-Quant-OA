# Documentation

### How to run the script?

This explains in detail how to run the script with your own email template and data source and also how the script works in general.

- Explains input

- Explains runtime complexities

- Explains output

### Code Structure

This explains the structure of the program and how it works.

### Dealing with patterns and custom patterns

- Default patterns are set to an open pattern: \_[ and a close pattern: ]\_.

- Pattern customization requires user to provide both an open and close pattern.

- Open and close patterns each needs to have 5 or less characters.

- Tolerance need to be less than the minimum length of open or close pattern.

- Dealing with warnings, to notify user that the template might have an incorrectly written pattern by using a default tolerance of one character. If a pattern set is found on the template with a single charcter tolerance missing on either the open or close pattern, the program will flag this as a warning and notify the user.

### Sanity Checks and Edge Cases Considered:

- Make sure the email_filler object is created with a template in either a .md extension or .txt extension. Other formats can easily be supported in the future, but in order to ensure our program runs as expected, we need to handle these specific cases.

- The source data in which we use to stub out the fillers are supposed to be given in a CSV format. We handle this by raising an error if it's otherwise.

- Ensure the source data has all the necessary patterns in the template file by raising an exception if this is not fullfilled. Raise a warning log if the source data has more columns than the required patterns in teh template which might indicate that the template is missing some patterns. This assumption holds as we consider the template to have priority over the source data as we need to completely fill the template thus giving only a warning if the template does not use all the source data but raising an error and stopping the program if the source data could not fill in all the patterns in the template. This check is done before running the parse/fill method.

- Handle Case Sensitivity in the pattern and columns from both template and source data by comparing them all in lower case.

- Make sure that the "to" and pattern column does not have a null value in the source_data as we need a recepient for the email.

- The cc and bcc columns are allowed to contain null values.

- Make sure the tolerance of pattern are greater than the minimum length of open and close pattern as we might have different lengths for both. And we still want to leave characters for the patterns.

- Make sure to check that the csv file is in the correct format

### Test Cases

This is stubbed out

### Exception explanations

This is stubbed out

### Libraries used

In order to NOT reinvent the wheel and become more efficient, I relied on stable and trusted libraries. I have decided to utilize the following libraries:

- Regex

- Pandas

### Python Style Guide:

- For styling the code base, I chose to adhere to the Google Style Guide (https://google.github.io/styleguide/pyguide.html) and I use yapf linting tool for Python that quickly transforms your code to an easily readable code base, loved by many developers and used by many teams at Google.
