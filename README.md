# Data Engineering Portfolio

Welcome to our sample Data Engineering portfolio!

# Projects

### bike-rental-data-management ([writeup](./bike-rental-data-management/writeup.md))

A relational database with analytics-ready views connecting Citi Bike and weather datasets. The project involved:
- inspecting and cleaning both datasets
- developing a relational database structure
- implementing the database in PostgreSQL and inserting the dataset
- developing flexible analytics-ready views on top of the relational database

### subscriber-pipeline ([writeup](./subscriber-pipeline/writeup/article.md))

A semi-automated bash+python pipeline to regularly transform a messy SQLite database into a clean source of truth for an analytics team. The pipeline
- performs unit tests to confirm data validity
- writes human-readable errors to an error log
- automatically checks and updates changelogs
- updates a production database with new clean data

### nosql-cloud-deployment ([writeup](./nosql-cloud-deployment))

A project to deploy the output of `subscriber-pipeline` to a MongoDB database on DigitalOcean Cloud. The project included
- creating a new MongoDB instance on DigitalOcean
- connecting to the cloud MongoDB using MongoDB Compass
- uploading the clean dataset as a NoSQL Collection
- validating the final dataset
