--- create a table with various daily ride counts
CREATE VIEW daily_counts AS
SELECT date_dim.date_key,
    date_dim.full_date,
    date_dim.month_name,
    date_dim.day,
    date_dim.day_name,
    date_dim.weekend,
    count(rides.id) AS ride_totals,
    count(trip_demo.user_type) filter (where trip_demo.user_type = 'Subscriber') as subscriber_rides,
    count(trip_demo.user_type) filter (where trip_demo.user_type = 'Customer') AS customer_rides,
    count(trip_demo.user_type) filter (where trip_demo.user_type = 'Unknown')  unknown_rides,
    count(rides.valid_duration) filter (where not rides.valid_duration) AS late_return
   FROM rides
     RIGHT JOIN date_dim ON rides.date_key = date_dim.date_key
     LEFT JOIN trip_demo ON rides.trip_demo = trip_demo.id
  GROUP BY date_dim.date_key
  ORDER BY date_dim.date_key;

 --- create a table with daily daily_data
 CREATE VIEW daily_data AS
 SELECT daily_counts.date_key,
    daily_counts.full_date,
    daily_counts.month_name,
    daily_counts.day,
    daily_counts.day_name,
    daily_counts.ride_totals,
    sum(daily_counts.ride_totals) OVER (PARTITION BY daily_counts.month_name ORDER BY daily_counts.date_key) AS month_running_total,
    daily_counts.subscriber_rides,
    daily_counts.customer_rides,
    daily_counts.unknown_rides,
    daily_counts.late_return,
    daily_counts.weekend,
    weather.tmin,
    weather.tavg,
    weather.tmax,
    weather.avg_wind,
    weather.prcp,
    weather.snow_amt,
    weather.rain,
    weather.snow
   FROM daily_counts
     JOIN weather ON daily_counts.date_key = weather.date_key
  ORDER BY daily_counts.date_key;

 --- create a monthly data view
 CREATE VIEW monthly_data AS
 SELECT date_dim.month,
    date_dim.month_name,
    round(avg(daily.ride_totals)) AS avg_daily_rides,
    sum(daily.ride_totals) AS total_rides,
    round(avg(daily.customer_rides)) AS avg_customer_rides,
    sum(daily.customer_rides) AS total_customer_rides,
    round(avg(daily.subscriber_rides)) AS avg_subscriber_rides,
    sum(daily.subscriber_rides) AS total_subscriber_rides,
    sum(daily.unknown_rides) AS total_unknown_rides,
    sum(daily.late_return) AS total_late_returns,
    round(avg(daily.tavg)) AS avg_tavg,
    count(daily.snow) FILTER (WHERE daily.snow) AS days_with_snow,
    count(daily.rain) FILTER (WHERE daily.rain) AS days_with_rain,
    max(daily.snow_amt) AS max_snow_amt,
    max(daily.prcp) AS max_prcp
   FROM date_dim
     JOIN daily_data daily ON date_dim.date_key = daily.date_key
  GROUP BY date_dim.month, date_dim.month_name
  ORDER BY date_dim.month;

--- create a view to help analyze rides returned after the limit
CREATE VIEW late_return AS
SELECT date_dim.full_date,
   rides.id,
   rides.trip_hours,
   rides.bike_id,
   ( SELECT stations.station_name
          FROM stations
         WHERE rides.start_station_id = stations.id) AS start_location,
   ( SELECT stations.station_name
          FROM stations
         WHERE rides.end_station_id = stations.id) AS end_location,
   trip_demo.user_type
  FROM rides
    JOIN date_dim ON rides.date_key = date_dim.date_key
    JOIN trip_demo ON rides.trip_demo = trip_demo.id
 WHERE rides.valid_duration = False;


--- examples of queries analysts could run on this database

 --- create a week summary over the year
 CREATE VIEW week_summary AS
 SELECT daily.day_name,
    round(avg(daily.ride_totals)) AS avg_rides,
    round(avg(daily.customer_rides)) AS avg_customer_rides,
    round(avg(daily.subscriber_rides)) AS avg_subscriber_rides
   FROM daily_counts daily
  GROUP BY daily.day_name
  ORDER BY (round(avg(daily.ride_totals))) DESC;

--- create an hourly summary
CREATE VIEW hourly_summary AS
SELECT EXTRACT(hour FROM rides.start_time) AS start_hour,
    count(*) AS ride_totals
   FROM rides
  GROUP BY (EXTRACT(hour FROM rides.start_time))
  ORDER BY (count(*)) DESC;

--- create a demographics summary
CREATE VIEW trip_demographics AS
SELECT count(rides.id) AS total_rides,
   trip_demo.age,
   trip_demo.gender,
   trip_demo.user_type
  FROM rides
    JOIN trip_demo ON rides.trip_demo = trip_demo.id
 GROUP BY trip_demo.age, trip_demo.gender, trip_demo.user_type
 ORDER BY trip_demo.user_type, trip_demo.gender, trip_demo.age;
