### Libraries used

In order to NOT reinvent the wheel and become more efficient by relying on stable and trusted libraries, I have decided to utilize the following libraries:

- Regex

- Pandas

### Code Base Structure

- Stubbed

### Python Style Guide:

- For styling the code base, I chose to adhere to the Google Style Guide (https://google.github.io/styleguide/pyguide.html) and I use yapf linting tool for Python that transforms your code to a quick and easily read code base, loved by many developers and used by many teams at Google.

### Sanity Checks and edge cases considered:

- Make sure the email_filler object is created with a template in either a .md extension or .txt extension. Other formats can easily be supported in the future, but in order to ensure our program runs as expected, we need to handle specific cases.

- The source data in which we use to stub out the fillers are supposed to be given in a CSV format. We handle this by raising an error if it's otherwise.
