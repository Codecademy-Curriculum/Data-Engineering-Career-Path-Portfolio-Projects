# Subscriber Cancellations Data Pipeline project

This repository contains example code to complete the Codecademy `Subscriber Cancellations Data Pipeline` Project.

## Project Description

A semi-automated bash+python pipeline to regularly transform a messy SQLite database into a clean source of truth for an analytics team.

The pipeline

- performs unit tests to confirm data validity
- writes human-readable errors to an error log
- automatically checks and updates changelogs
- updates a production database with new clean data

Please see [writeup/article.md](https://github.com/Codecademy-Curriculum/Data-Engineering-Career-Path-Portfolio/blob/main/subscriber-pipeline/writeup/article.md) for an overview of the development process and [writeup/data_eng_cp_writeup.ipynb](https://github.com/Codecademy-Curriculum/Data-Engineering-Career-Path-Portfolio/blob/main/subscriber-pipeline/writeup/data_eng_cp_writeup.ipynb) for an exploratory Jupyter notebook.

## Instructions

This repository is set up as if the scripts have never been run. To run,

1. Run `script.sh` and follow the prompts
2. If prompted, `script.sh` will run `dev/cleanse_data.py`, which runs unit tests and data cleaning functions on `dev/cademycode.db`
3. If `cleanse_data.py` runs into any errors during unit testing, it will raise an exception, log the issue, and terminate
4. Otherwise, `cleanse_data.py` will update the clean database and CSV with any new records
5. After a successful update, the number of new records and other update data will be written to `dev/changelog.md`
6. `script.sh` will check the changelog to see if there are updates
7. If so, `script.sh` will request permission to overwrite the production database
7. If the user grants permission, `script.sh` will copy the updated database to `prod`

If you follow these instructions, the script will run on the initial dataset in `dev/cademycode.db`. To test running the script on the updated database, change the name of `dev/cademycode_updated.db` to `dev/cademycode.db`.

## Folder Structure
- **script.sh**: bash script to handle running the data cleanser and moving files to `/prod`
### dev
- **changelog.md**: automatically updated with each run, logs new records and tracks missing data
- **cleanse_data.py**: runs unit tests and data cleansing on `cademycode.db`.
- **cleanse_db.log**: log of errors encountered during the python script execution.
- **cademycode_cleansed.db**: output from `cleanse_data.py` that contains 2 tables
    - `cademycode_aggregated`: table containing the joined data from cleaned version of the 3 `cademycode.db` tables.
    - `missing_data`: table containing incomplete data that could not be imputed or assumed.
- **cademycode.db**: database containing the raw data from 3 tables:
    - `cademycode_students`: demographic and course data of mock cademycode students.
    - `cademycode_student_jobs`: a lookup table of student job industries.
    - `cademycode_courses`: a lookup table of career paths and the estimated hours of completion.
- **cademycode_updated.db**: updated version of `cademycode.db` for testing the update process
### prod
- **changelog.md**: `script.sh` will copy from `/dev` when updates are approved
- **cademycode_cleansed.db**:  `script.sh` will copy from `/dev` when updates are approved
- **cademycode_cleansed.csv**: CSV version of the clean table, overwritten upon update
### writeup
- **article.md**: high-level overview of the process of developing these scripts
- **data_eng_cp_writeup.ipynb**: Jupyter Notebook containing the discovery phase of this project: loading, inspecting, transforming.
