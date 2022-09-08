# Bike Rental Data Management Writeup

## Project Overview

The last decade has seen enormous growth in the personal transportation startup industry, including bike and e-bike rental programs in many major cities. The goal of this project is to create a flexible and efficient relational database to store bike rental data, using datasets from Citi Bike and NOAA. The project involved

- inspecting and cleaning both datasets
- developing a relational database structure
- implementing the database in PostgreSQL and inserting the data
- developing flexible analytics-ready views on top of the relational database

## Inspecting and Cleaning the Datasets

#### [Jupyter Notebook](./bike-rental.ipynb)

The datasets for this project were monthly Citi Bike trip records from Jersey City and daily NOAA weather data from Newark Airport. Both datasets were for the full year of 2016.

The Citi Bike dataset had some data integrity issues. Four days were missing from the data altogether, and a few fields had missing or unknown values. Visualization and statistical analysis indicated that the missing values were likely not missing at random. For example, demographic information was almost entirely missing for short-term customers. To help the analytics team investigate these issues, I preserved the missing data as `unknown` and created summary columns in the final database so that the missing data can be easily used or removed.

There were also outliers in some of the numeric fields. For example, the trip duration column had trips lasting thousands of hours, even though Citi Bike's maximum rental is 24 hours. Since it was possible these indicated system malfunctions or users keeping rentals past the limit, I kept these values in the dataset and created a flag to easily access them or remove them from queries. I also created fields to view trip duration by minutes and hours (the original dataset had only seconds.)

The weather dataset had some all-null columns that needed to be dropped, leaving average wind speed, precipitation, temperature, snow depth and snow amount. These are all fields one might expect to impact bike ridership in measurable ways. I also added binary rain and snow indicators to assist in filtering views.

## Developing and Implementing a Relational Database

#### [Entity Relationship Diagram](./ERD.pdf), [SQL create table queries](./tables.sql)

The Citi Bike table required some adjustment for normalization. For example, the `station` and `demographic` data needed to be split into their own tables. The station data already had IDs in the database to reuse as a key, while the demographic data required creating a new primary key column and adding the appropriate pointers in the main Citi Bike table.

The weather data required less restructuring. However, joining on date-time fields is risky. To facilitate joins, I created a `date_key` field for both the weather and Citi Bike data that stores each day as an integer in `yyyymmdd` format.

Finally, I created a central date dimension table to easily and efficiently provide different date information. This table stores each day as both a date and integer `date_key` along with:

- month as both number (e.g. `1`) and name (`January`)
- day as both number (e.g `21`) and name (`Wednesday`)
- whether the day is a weekend day or not
- the financial quarter

Based on these tables, I created a database schema specifying data types and primary/foreign key relationships. After creating a PostgreSQL database matching this schema, I used SQLAlchemy and pandas to insert the data to the database.

## Developing Views

#### [SQL create view queries](./views.sql)

To assist an analytics team, I developed the following views:

### daily_data

This view contains data for every day of the year (using outer joins to make sure days missing from the Citi Bike dataset can be investigated).  In addition to the number of rides on a given day, it contains

- date breakdowns (e.g. month and day of the week)
- ride breakdowns (e.g. using `filter` statements to see rides by subscriber, customer, and duration)
- running monthly totals (using `window` functions)
- and weather data

In particular, this view contains data on the number of records with unknown `user_type` and suspiciously large `trip_duration`. This should help an analytics team investigate these further.

### monthly_data

This view summarizes `daily_data` by month. In addition to the number of rides per month, it contains
- total rides broken down by user type
- daily ride averages broken down by user type
- average temperature and maximum precipitation amounts (since averages were all close to `0`)
- counts of rainy and snowy days

### late_return

While the prior views already contain counts of late returns (rentals with a duration over 24 hours), this table contains the data needed to investigate these further:
- full date
- bike id
- start and end station
- user type

### hourly_summary, trip_demographics, week_summary

In addition to the main views, I created some smaller views. These are examples of the kinds of analytics that can be built on top of this database. They include summaries of trip demographics as well as the most popular hours of the day and days of the week.
