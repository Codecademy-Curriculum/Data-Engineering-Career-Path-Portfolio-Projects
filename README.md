# Data Engineering Portfolio

Welcome to our sample Data Engineering portfolio!

# Projects

### subscriber-pipeline ([writeup](https://github.com/Codecademy-Curriculum/Data-Engineering-Career-Path-Portfolio/blob/main/subscriber-pipeline/writeup/article.md))

A semi-automated bash+python pipeline to regularly transform a messy SQLite database into a clean source of truth for an analytics team. The pipeline
- performs unit tests to confirm data validity
- writes human-readable errors to an error log
- automatically checks and updates changelogs
- updates a production database with new clean data

### nosql-cloud-deployment ([writeup](https://github.com/Codecademy-Curriculum/Data-Engineering-Career-Path-Portfolio/tree/main/nosql-cloud-deployment))

A project to deploy the output of `subscriber-pipeline` to a MongoDB database on DigitalOcean Cloud. The project included
- creating a new MongoDB instance on DigitalOcean
- connecting to the cloud MongoDB using MongoDB Compass
- uploading the clean dataset as a NoSQL Collection
- validating the final dataset
