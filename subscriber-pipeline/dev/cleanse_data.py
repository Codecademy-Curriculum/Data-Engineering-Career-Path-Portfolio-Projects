#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import ast
import numpy as np
from sqlalchemy import create_engine
import logging

pd.options.mode.chained_assignment = None

logging.basicConfig(filename="./dev/cleanse_db.log",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filemode='w',
                    level=logging.DEBUG,
                    force=True)
logger = logging.getLogger(__name__)


def cleanse_student_table(df):
    """
    Cleanse the `cademycode_students` table according to the discoveries made in the writeup

    Parameters:
        df (DataFrame): `student` table from `cademycode.db`

    Returns:
        df (DataFrame): cleaned version of the input table
        missing_data (DataFrame): incomplete data that was removed for later inspection

    """
    now = pd.to_datetime('now')
    df['age'] = (now - pd.to_datetime(df['dob'])).astype('<m8[Y]')
    df['age_group'] = np.int64((df['age']/10))*10

    df['contact_info'] = df["contact_info"].apply(lambda x: ast.literal_eval(x))
    explode_contact = pd.json_normalize(df['contact_info'])
    df = pd.concat([df.drop('contact_info', axis=1).reset_index(drop=True), explode_contact], axis=1)

    split_address = df.mailing_address.str.split(',', expand=True)
    split_address.columns = ['street', 'city', 'state', 'zip_code']
    df = pd.concat([df.drop('mailing_address', axis=1), split_address], axis=1)

    df['job_id'] = df['job_id'].astype(float)
    df['current_career_path_id'] = df['current_career_path_id'].astype(float)
    df['num_course_taken'] = df['num_course_taken'].astype(float)
    df['time_spent_hrs'] = df['time_spent_hrs'].astype(float)

    missing_data = pd.DataFrame()
    missing_course_taken = df[df[['num_course_taken']].isnull().any(axis=1)]
    missing_data = pd.concat([missing_data, missing_course_taken])
    df = df.dropna(subset=['num_course_taken'])

    missing_job_id = df[df[['job_id']].isnull().any(axis=1)]
    missing_data = pd.concat([missing_data, missing_job_id])
    df = df.dropna(subset=['job_id'])

    df['current_career_path_id'] = np.where(df['current_career_path_id'].isnull(), 0, df['current_career_path_id'])
    df['time_spent_hrs'] = np.where(df['time_spent_hrs'].isnull(), 0, df['time_spent_hrs'])

    return(df, missing_data)


def cleanse_career_path(df):
    """
    Cleanse the `cademycode_courses` table according to the discoveries made in the writeup

    Parameters:
        df (DataFrame): `cademycode_courses` table from `cademycode.db`

    Returns:
        df (DataFrame): cleaned version of the input table

    """
    not_applicable = {'career_path_id': 0,
                      'career_path_name': 'not applicable',
                      'hours_to_complete': 0}
    df.loc[len(df)] = not_applicable
    return(df.drop_duplicates())


def cleanse_student_jobs(df):
    """
    Cleanse the `cademycode_student_jobs` table according to the discoveries made in the writeup

    Parameters:
        df (DataFrame): `cademycode_student_jobs` table from `cademycode.db`

    Returns:
        df (DataFrame): cleaned version of the input table

    """
    return(df.drop_duplicates())


def test_for_path_id(students, career_paths):
    """
    Unit test to ensure that join keys exist between the students and courses tables

    Parameters:
        students (DataFrame): `cademycode_student_jobs` table from `cademycode.db`
        career_paths (DataFrame): `cademycode_courses` table from `cademycode.db`

    Returns:
        None
    """
    student_table = students.current_career_path_id.unique()
    is_subset = np.isin(student_table, career_paths.career_path_id.unique())
    missing_id = student_table[~is_subset]
    try:
        assert len(missing_id) == 0, "Missing career_path_id(s): " + str(list(missing_id)) + " in `career_paths` table"
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('All career_path_ids are present.')


def test_for_job_id(students, student_jobs):
    """
    Unit test to ensure that join keys exist between the students and student_jobs tables

    Parameters:
        students (DataFrame): `cademycode_student_jobs` table from `cademycode.db`
        student_jobs (DataFrame): `cademycode_student_jobs` table from `cademycode.db`

    Returns:
        None
    """
    student_table = students.job_id.unique()
    is_subset = np.isin(student_table, student_jobs.job_id.unique())
    missing_id = student_table[~is_subset]
    try:
        assert len(missing_id) == 0, "Missing job_id(s): " + str(list(missing_id)) + " in `student_jobs` table"
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('All job_ids are present.')


def test_nulls(df):
    """
    Unit test to ensure that no rows in the cleaned table are null

    Parameters:
        df (DataFrame): DataFrame of the cleansed table

    Returns:
        None
    """
    df_missing = df[df.isnull().any(axis=1)]
    cnt_missing =len(df_missing)

    try:
        assert cnt_missing == 0, "There are " + str(cnt_missing) + " nulls in the table"
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('No null rows found.')


def test_num_cols(local_df, db_df):
    """
    Unit test to ensure that the number of columns in the cleaned DataFrame match the
    number of columns in the SQLite3 database table.

    Parameters:
        local_df (DataFrame): DataFrame of the cleansed table
        db_df (DataFrame): `cademycode_aggregated` table from `cademycode_cleansed.db`

    Returns:
        None
    """
    try:
        assert len(local_df.columns) == len(db_df.columns)
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('Number of columns are the same.')


def test_schema(local_df, db_df):
    """
    Unit test to ensure that the column dtypes in the cleaned DataFrame match the
    column dtypes in the SQLite3 database table.

    Parameters:
        local_df (DataFrame): DataFrame of the cleansed table
        db_df (DataFrame): `cademycode_aggregated` table from `cademycode_cleansed.db`

    Returns:
        None
    """
    errors = 0
    for col in db_df:
        try:
            if local_df[col].dtypes != db_df[col].dtypes:
                errors+=1
        except NameError as ne:
            logger.exception(ne)
            raise ne

    if errors > 0:
        assert_err_msg = str(errors) + " column(s) dtypes aren't the same"
        logger.exception(assert_err_msg)
    assert errors == 0, assert_err_msg


def main():

    # initialize log
    logger.info("Start Log")

    # check for current version and calculate next version for changelog
    with open('./dev/changelog.md') as f:
        lines = f.readlines()
    next_ver = int(lines[0].split('.')[2][0])+1

    # connect to the dev database and read in the three tables
    con = sqlite3.connect('./dev/cademycode.db')
    students = pd.read_sql_query("SELECT * FROM cademycode_students", con)
    career_paths = pd.read_sql_query("SELECT * FROM cademycode_courses", con)
    student_jobs = pd.read_sql_query("SELECT * FROM cademycode_student_jobs", con)
    con.close()

    # get the current production tables, if they exist
    try:
        con = sqlite3.connect('./prod/cademycode_cleansed.db')
        clean_db = pd.read_sql_query("SELECT * FROM cademycode_aggregated", con)
        missing_db = pd.read_sql_query("SELECT * FROM incomplete_data", con)
        con.close()

        # filter for students that don't exist in the cleansed database
        new_students = students[~np.isin(students.uuid.unique(), clean_db.uuid.unique())]
    except:
        new_students = students
        clean_db = []

    # run the cleanse_student_table() function on the new students only
    clean_new_students, missing_data = cleanse_student_table(new_students)

    try:
        # filter for incomplete rows that don't exist in the missing data table
        new_missing_data = missing_data[~np.isin(missing_data.uuid.unique(), missing_db.uuid.unique())]
    except:
        new_missing_data = missing_data

    # upsert new incomplete data if there are any
    if len(new_missing_data) > 0:
        sqlite_connection = sqlite3.connect('./dev/cademycode_cleansed.db')
        missing_data.to_sql('incomplete_data', sqlite_connection, if_exists='append', index=False)
        sqlite_connection.close()

    # proceed only if there is new student data
    if len(clean_new_students) > 0:
        # clean the rest of the tables
        clean_career_paths = cleanse_career_path(career_paths)
        clean_student_jobs = cleanse_student_jobs(student_jobs)

        ##### UNIT TESTING BEFORE JOINING #####
        # Ensure that all required join keys are present
        test_for_job_id(clean_new_students, clean_student_jobs)
        test_for_path_id(clean_new_students, clean_career_paths)
        #######################################

        clean_new_students['job_id'] = clean_new_students['job_id'].astype(int)
        clean_new_students['current_career_path_id'] = clean_new_students['current_career_path_id'].astype(int)

        df_clean = clean_new_students.merge(clean_career_paths, left_on='current_career_path_id', right_on='career_path_id', how='left')
        df_clean = df_clean.merge(clean_student_jobs, on='job_id', how='left')

        ##### UNIT TESTING #####
        # Ensure correct schema and complete data before upserting to database
        if len(clean_db) > 0:
            test_num_cols(df_clean, clean_db)
            test_schema(df_clean, clean_db)
        test_nulls(df_clean)
        ########################

        # Upsert new cleaned data to cademycode_cleansed.db
        con = create_engine('sqlite:///./dev/cademycode_cleansed.db', echo=True)
        sqlite_connection = con.connect()
        df_clean.to_sql('cademycode_aggregated', sqlite_connection, if_exists='append', index=False)
        clean_db = pd.read_sql_query("SELECT * FROM cademycode_aggregated", con)
        sqlite_connection.close()

        # Write new cleaned data to a csv file
        clean_db.to_csv('./dev/cademycode_cleansed.csv')

        # create new automatic changelog entry
        new_lines = [
            '## 0.0.' + str(next_ver) + '\n' +
            '### Added\n' +
            '- ' + str(len(df_clean)) + ' more data to database of raw data\n' +
            '- ' + str(len(new_missing_data)) + ' new missing data to incomplete_data table\n' +
            '\n'
        ]
        w_lines = ''.join(new_lines + lines)

        # update the changelog
        with open('./dev/changelog.md', 'w') as f:
            for line in w_lines:
                f.write(line)
    else:
        print("No new data")
        logger.info("No new data")
    logger.info("End Log")


if __name__ == "__main__":
    main()
