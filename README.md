# sqlalchemy-challenge
## Trip planning for a long holiday vacation in Honolulu, Hawaii.

### Part 1: Analyze and Explore the Climate Data

In this section, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of the provided climate database. Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, I completed the following steps:

* I used the provided files (climate_starter.ipynb and hawaii.sqlite) to complete my climate analysis and data exploration.
* I used the SQLAlchemy create_engine() function to connect to the SQLite database.
* I used the SQLAlchemy automap_base() function to reflect the tables into classes, and then save references to the classes named station and measurement.
* I linked Python to the database by creating a SQLAlchemy session.
* I then performed a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

### Precipitation Analysis:
1. I retrieved the most recent date in the dataset.
2. Using that date, I get the previous 12 months of precipitation data by querying the previous 12 months of data. The code is written to dynamically retrieve the dates required. 
3. I selected only the "date" and "prcp" values.
4. The query results were then loaded into a Pandas DataFrame. I explicitly set the column names.
5. I then sorted the DataFrame values by "date". 
6. I ploted the results by using the DataFrame plot method. 
7. I then used Pandas to print the summary statistics for the precipitation data. 

### Station Analysis:

1. I designed a query to calculate the total number of stations in the dataset.
2. I designed another query to find the most-active stations (that is, the stations that have the most rows). 
3. Another query calculated the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
4. I then designed a query to get the previous 12 months of temperature observation (TOBS) data. I filtered the data by the station that has the greatest number of observations. I then queried the previous 12 months of TOBS data for that station. The results were then plotted as a histogram with 12 bins. 

*I concluded the above two sections by closing the session.*

### Part 2: Designing a Climate App 

In this section I designed a Flask API based on the queries that I developed in the first part of this project.

The flask was created as follows: 
1. /
Starts at the homepage.
Lists all the available routes.

2. /api/v1.0/precipitation
Converts the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
Returns the JSON representation of the dictionary.

3. /api/v1.0/stations
Returns a JSON list of stations from the dataset.

4. /api/v1.0/tobs
Queries the dates and temperature observations of the most-active station for the previous year of data.
Returns a JSON list of temperature observations for the previous year.

5. /api/v1.0/<start>  
Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date. 
For a specified start, it shows tesults of the calculations for TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

6. /api/v1.0/<start>/<end>
For a specified start date and end date, it shows tesults of the calculations for TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

*References*
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml