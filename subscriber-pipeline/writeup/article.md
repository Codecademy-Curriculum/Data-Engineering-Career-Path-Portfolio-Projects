# Project Writeup

A semi-automated bash+python pipeline to regularly transform a messy SQLite database into a clean source of truth for an analytics team. The pipeline
- performs unit tests to confirm data validity
- writes human-readable errors to an error log
- automatically checks and updates changelogs
- updates a production database with new clean data

## Scenario

A fictional online education company `Cademycode` has a database of cancelled subscriber information that gets periodically updated from a variety of sources (to be clear: this data is entirely fictional). They want to automate the process of transforming this messy database into a clean table for their analytics team. My goal was to create a semi-automated data ingestion pipeline that checks for new data, automatically performs cleaning and transformation operations, runs unit tests to check data validity, and logs errors for human review.

## The Process

### Inspecting and Transforming the Dataset ([exploration notebook](https://github.com/Codecademy-Curriculum/Data-Engineering-Career-Path-Portfolio/blob/main/subscriber-pipeline/writeup/data_eng_cp_writeup.ipynb))

Several of the raw data tables had records with some missing data. Visualization indicated that most of the missing data was missing at random (MAR). Because this data was MAR and formed only a small percentage of the overall data, deletion seemed appropriate. Instead of fully deleting the missing rows, I separated the rows with missing data into their own table. This way, an analytics team can inspect the missing data themselves if they want, and we can keep track of how much data is missing as the cleaned database was updated.

Some of the missing data was structurally missing, corresponding to students who had never started any courses before cancelling their subscription. I handled these rows by introducing a new category for those students, so an analytics team can easily study subscribers who cancel before making any use of the product.

In addition to missing data, the student's contact information was stored in a dictionary, which needed to be converted to flat columns with the correct data types.

Lastly, I added new columns to assist an analytics team in filtering the subscriber population. For example, I used the subscriber birth date to create age and decade categories, so an analytics team can more easily see if those demographic attributes impact subscribers.

### Automation

The raw database is updated regularly with new long-term cancellations, so the transformations above need to automated as much as possible. However, an automated data process also needs automated checks to prevent unwanted data updates. Therefore, the cleaning and wrangling code needed to be wrapped in a Python script to perform unit tests, log errors, and track any features of potential concern (such as a sudden increase in records with missing entries.)

My unit tests check

- If there are any updates to the database
- If there are any new rows with missing values in the updates
- If there are any fully null rows in the updates
- If the table schemas are the same as expected
- If all join keys are present between the tables before joining

If the process passes all the tests, I can be reasonably confident that the automated cleaning script will operate as I expect from my Jupyter notebook, and the update can proceed. If not, then logged errors help me identify any unexpected changes to the database (for example, a new column) that my script wasn't designed to handle. Even if all unit tests are passed, the script still records data regarding missing records to the changelog for human review.

Lastly, I created a bash script to automate the process of

1. running the unit test and update script
2. checking if the script found and made any updates
3. if so, moving the newly updated clean database to a production folder
