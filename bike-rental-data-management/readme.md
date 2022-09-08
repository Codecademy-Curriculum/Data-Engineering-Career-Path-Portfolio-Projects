# bike-rental-data-management

This repository contains code to complete Codecademy's `Bike Rental Data Management` project.

## Project Overview

Project to create a relational database with analytics-ready views connecting Citi Bike and weather datasets. The project involved:
- inspecting and cleaning both datasets
- developing a relational database structure
- implementing the database in PostgreSQL and inserting the dataset
- developing flexible analytics-ready views on top of the relational database

# Folder Structure

- `bike-rental.ipynb`: prepare the data for inserting into the database
- `tables.sql`: SQL queries to create the database tables
- `views.sql`: SQL queries to create the database views
- `ERD.pdf`: entity relationship diagram for the database

### `data`
- `newark_airport_2016.csv`: weather data from Newark airport
- `JC-2016xx-citibike-tripdata.csv`: twelve files each containing one month of Citi Bike data from Jersey City
    - replace `xx` with the number of each month

### `data-dictionaries`
- `citibike.pdf`: details on the Citi Bike data files from Citi Bike's website
- `weather.pdf`: details on the weather data from NOAA's website
