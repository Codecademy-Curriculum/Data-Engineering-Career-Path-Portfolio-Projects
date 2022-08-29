# NoSQL Cloud Deployment

## Project writeup

In this project, I deployed the output from my `subscriber-pipeline` project to a MongoDB database on DigitalOcean. The project included

- creating a new MongoDB instance on DigitalOcean
- connecting to the cloud MongoDB using MongoDB Compass
- uploading the clean dataset as a NoSQL Collection
- validating the final dataset

### Database Setup

1. Create a MongoDB instance on DigitalOcean
2. Connect to the MongoDB instance from MongoDB Compass
3. Create a new database on the server
4. Collect the output CSV from `subscriber-pipeline`
5. Import the CSV as a NoSQL collection with the correct datatypes

### Database Validation

After importing the data, I performed the following validation checks

1. To confirm no data was lost, I compared row counts between the CSV and the MongoDB Database
2. I inspected a few records visually, and noticed some whitespace had been introduced. I can use a `$trim` aggregation after import to remove this whitespace in the MongoDB, though it would be better to investigate exactly where these artifacts were introduced in the full pipeline.
3. I created the following analytics-oriented filters to inspect the results:
    1. `{state: {$eq: " Colorado"}}` to see a specific state (notice the whitespace issue appearing here)
    2. `{avg_salary: {$gt: 100000}}` to see customers from high-earning industries
    3. `{time_spent_hrs: {$eq: 0}}` to see customers who cancelled before spending any time on the platform
