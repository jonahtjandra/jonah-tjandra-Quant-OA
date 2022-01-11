from email_filler import EmailFiller


def main():
    parser = EmailFiller("../email-filler-script/email_template.md",
                         "./sample_data/sample.csv")
    parser.fill_template("stub", "stub")


main()