import time
Start_Time_Main = time.time()
import mysql.connector as msql # pip install mysql-connector-python
from mysql.connector import Error
import pandas as pd
import sys
import csv

source_filename = "clean.csv"
delimiter = ";"

# Function to establish SQL connection, create pollution-db2 database and connect to it
def Initialise_SQL(host_name, database_name, username, password):
    # Establishing SQL server connection
    try:
        SQL_Initialize = msql.connect(
            host=host_name,
            user=username,
            passwd=password
        )
        if SQL_Initialize.is_connected():
            print("SQL server connection: Successful") # Printing the connection status to SQL server
    except Error as err:
        print("Error connecting to SQL server : ", err)
        sys.exit()
    # Creating pollution-db2 database
    else:
        try:
            SQL_Cursor = SQL_Initialize.cursor()
            # Creating pollution-db2 database
            Drop_Database_Query = "DROP DATABASE IF EXISTS `{}`;".format(database_name) # Query to drop any existing databases with the same name
            Create_Database_Query = "CREATE DATABASE `{}`;".format(database_name) # Query to create the desired database
            SQL_Cursor.execute(Drop_Database_Query) # Dropping any existing databases
            SQL_Cursor.execute(Create_Database_Query) # Creating pollution-db2 database
        except Error as err:
            print("Error creating {} database: ".format(database_name), err)
            sys.exit()
        else:
            print("Created pollution-db2 database")
            # Connecting to pollution-db2 database
            try:
                SQL_Initialize = msql.connect(
                    host=host_name,
                    database=database_name,
                    user=username,
                    passwd=password
                )
                if SQL_Initialize.is_connected():
                    print("Connected to pollution-db2 database") # Printing the connection status to pollution-db2 database
            except Error as err:
                print("Error connecting to {} database: ".format(database_name), err)
                sys.exit()
            else:
                return SQL_Initialize
Initialisation_key = Initialise_SQL('localhost', 'pollution-db2', 'root', '')
SQL_Cursor = Initialisation_key.cursor()

# Function to execute a multiple SQL queries
def Execute_Query(SQL_Cursor, Initialisation_key, Query):
    try:
        for query_i in Query:
            SQL_Cursor.execute(query_i)
            Initialisation_key.commit()
    except Error as err:
        print("Error executing the query: ", err)
        sys.exit()

# Creating the "Site" table
start_time = time.time()
add_nulls = lambda value : value or None # function to convert missing values to "None"
try:
    # Writing a query to create the Site table
    Create_Site_Query = ["""DROP TABLE IF EXISTS `pollution-db2`.`Site`;""", """CREATE TABLE IF NOT EXISTS `pollution-db2`.`Site` (
        `SiteID` INT NOT NULL,
        `Location` VARCHAR(128) NOT NULL,
        `Latitude` DECIMAL(18,16) NULL,`Longitude` DECIMAL(19,16) NULL,
        PRIMARY KEY (`SiteID`))
    ENGINE = InnoDB;"""]
    Execute_Query(SQL_Cursor, Initialisation_key, Create_Site_Query) # Creating the Site table
except Error as err:
    print("Error creating Site table: ", err)
    sys.exit()
else:
    print("Created Site table header")
    
# Populating the "Site" table in the pollution-db2 database
# Removing duplicate SiteID entries
try:
    Site_Data = pd.read_csv(source_filename, sep=delimiter,low_memory=False, usecols=["SiteID", "Location", "Latitude", "Longitude"]).drop_duplicates("SiteID", keep="last") 
except FileNotFoundError as err:
    print("No such file exists in the target directory: {}".format(source_filename),"\nPlease check the file name or make sure it exists the the target directory")
    print(err)
    sys.exit()
try:
    # Query to populate the Site table
    Populate_Site_Query = "INSERT INTO `pollution-db2`.`Site` VALUES (%s,%s,%s,%s);"
    for index, row in Site_Data.iterrows():
        # SQL by default replaces missing values with 0
        Clean_Row = [add_nulls(value) for value in row] # Converting missing values to None which are interpreted by the SQL server as Nulls
        SQL_Cursor.execute(Populate_Site_Query, tuple(Clean_Row)) # Populating Site table with required values
except Error as err:
    print("Error populating Site table: ", err)
    sys.exit()
else:
    Initialisation_key.commit() # Committing updates to the Site table
    print("Site table is populated with SiteID, Location, Latitude, Longitude values")
print("--- %s seconds ---" % (time.time() - start_time))

# Creating the "Reading" table
start_time = time.time()
try:
    # Writing a query to create the Reading table
    Create_Reading_Query = ["""DROP TABLE IF EXISTS `pollution-db2`.`Reading`;""", """CREATE TABLE IF NOT EXISTS `pollution-db2`.`Reading` (
        `MeasurementID` INT NOT NULL AUTO_INCREMENT,`Date` DATE NULL,`Time` TIME NULL,`Time Offset` TIME NULL,
        `NOx` DECIMAL(14,8) NULL,`NO2` DECIMAL(14,8) NULL,`NO` DECIMAL(14,8) NULL,`PM10` DECIMAL(14,8) NULL,
        `NVPM10` DECIMAL(14,8) NULL,`VPM10` DECIMAL(14,8) NULL,`NVPM2.5` DECIMAL(14,8) NULL,`PM2.5` DECIMAL(14,8) NULL,
        `VPM2.5` DECIMAL(14,8) NULL,`CO` DECIMAL(14,8) NULL,`O3` DECIMAL(14,8) NULL,`SO2` DECIMAL(14,8) NULL,
        `Temperature` DECIMAL(14,8) NULL,`RH` DECIMAL(14,8) NULL,`Air Pressure` DECIMAL(14,8) NULL,
        `DateStart` DATE NULL,`TimeStart` TIME NULL,`TimeStart Offset` TIME NULL,
        `DateEnd` DATE NULL,`TimeEnd` TIME NULL,`TimeEnd Offset` TIME NULL,
        `Current` VARCHAR(6) NULL,`Instrument Type` VARCHAR(128) NULL,`SiteID` INT NOT NULL,
        PRIMARY KEY (`MeasurementID`),
        INDEX `fk_Reading_Site_idx` (`SiteID` ASC),
        CONSTRAINT `fk_Reading_Site`
        FOREIGN KEY (`SiteID`)
        REFERENCES `pollution-db2`.`Site` (`SiteID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB;"""]
    Execute_Query(SQL_Cursor, Initialisation_key, Create_Reading_Query) # Creating the Reading table
except Error as err:
    print("Error creating Reading table: ", err)
    sys.exit()
else:
    print("Created Reading table header")
    
# Populating the "Reading" table in the pollution-db2 database
start_time = time.time()
# Chunk size defines the number of enteries (chunks) that are written to the Reading table per instance
Chunk_Size = 10000 # Optimum vlaue of chunk size depends on the configuration of the system
try:
    print("Loading measurement data into the Reading table...")
    row_count = 0
    # Query to populate the Reading table
    Populate_Reading_Query = "INSERT INTO `pollution-db2`.`Reading` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    Reading_Column_Indexes = list(range(0,6,1))+list(range(7,19,1))+list(range(22,30,1))+[6] # Extracting the indexes of the values to be inserted into the Reading table
    with open(source_filename, "r") as line_counter: # Counting the total number of lines which is used to print the percentage completion status
        line_count = 0
        for line in line_counter:
            line_count += 1
    with open(source_filename, "r") as csv_data:
        for row in csv.reader(csv_data, delimiter=delimiter):
            if row_count == 0:
                row_count += 1
                continue # Skipping the header row
            row = [row_count]+[row[i] for i in Reading_Column_Indexes] # row count is used to populate MeasurementID primary key. Remaining values are extracted from the each row read
            Clean_Row = [add_nulls(value) for value in row] # Converting missing values to None which are interpreted by the SQL server as Nulls
            SQL_Cursor.execute(Populate_Reading_Query, tuple(Clean_Row)) # Populating Reading table with the required values
            # This section is used to commit chunks of data based on the Chnk_Size value and to calculate and print the percentage completion status
            if row_count%Chunk_Size == 0:
                Initialisation_key.commit() # Committing updates to the Reading table
                print("--- {}% complete! ---".format(int(row_count/line_count*100)),end="\r")
            row_count += 1
except Error as err:
    print("\nError inserting row {} of clean.csv into the Reading table: ".format(row_count), err)
    sys.exit()
else:
    Initialisation_key.commit()
    print("--- {}% complete! ---".format(int(row_count/line_count*100)))
    print("\nSuccessfully inserted measurement data from {} into the Reading table in the pollution-db2 database".format("clean.csv"))
print("--- %s seconds ---" % (time.time() - start_time))


# Creating the "Pollution-Schema" table
start_time = time.time()
try:
    # Writing a query to create the Pollution-Schema table
    Create_Schema_Query = ["""DROP TABLE IF EXISTS `pollution-db2`.`Pollution-Schema`;""", """CREATE TABLE IF NOT EXISTS `pollution-db2`.`Pollution-Schema` (
        `SchemaID` INT NOT NULL AUTO_INCREMENT,
        `Measure` VARCHAR(128) NOT NULL,
        `Description` VARCHAR(512) NOT NULL,
        `Unit` NVARCHAR(12) NOT NULL,
        PRIMARY KEY (`SchemaID`))
    ENGINE = InnoDB;"""]
    Execute_Query(SQL_Cursor, Initialisation_key, Create_Schema_Query) # Creating the Pollution-Schema table
except Error as err:
    print("Error creating Pollution-Schema table: ", err)
    sys.exit()
else:
    print("Created Pollution-Schema table header")

# Populating the "Pollution-Schema" table in the pollution-db2 database
try:
    # Creating a data frame which consists of schema information
    schema = pd.DataFrame({'measure': ('Date','Time','Time Offset','NOx','NO2','NO','SiteID','PM10','NVPM10','VPM10','NVPM2.5','PM2.5','VPM2.5','CO','O3','SO2','Temperature','RH','Air Pressure','Location','Latitude','Longitude','DateStart','Time Start','Time Start Offset','DateEnd','Time End','Time End Offset','Current','Instrument Type'),
    'desc': ('Date of measurement','Time of measurement','Time offset of measurement','Concentration of oxides of nitrogen','Concentration of nitrogen dioxide','Concentration of nitric oxide','Site ID for the station','Concentration of particulate matter <10 micron diameter','Concentration of non - volatile particulate matter <10 micron diameter','Concentration of volatile particulate matter <10 micron diameter','Concentration of non volatile particulate matter <2.5 micron diameter','Concentration of particulate matter <2.5 micron diameter','Concentration of volatile particulate matter <2.5 micron diameter','Concentration of carbon monoxide','Concentration of ozone','Concentration of sulphur dioxide','Air temperature','Relative Humidity','Air Pressure','mbar''Text description of location','Latitude','Longitude','The date monitoring started','The time monitoring started','The time offset monitoring started','The date monitoring ended','The time monitoring ended','The time offset monitoring ended','Is the monitor currently operating','Classification of the instrument'),
    'unit': ('date','time','time','㎍/m3','㎍/m3','㎍/m3','integer','㎍/m3','㎍/m3','㎍/m3','㎍/m3','㎍/m3','㎍/m3','㎎/m3','㎍/m3','㎍/m3','°C','%','mbar','text','geo point','geo point','date','time','time','date','time','time','text','text')})
    # Query to populate the Pollution-Schema table
    Populate_Schema_Query = "INSERT INTO `pollution-db2`.`Pollution-Schema` (Measure, Description, Unit) VALUES (%s,%s,%s)"
    SQL_Cursor = Initialisation_key.cursor()
    print("Populating the Schema table in the pollution-db2 database with Schema information")
    # Reading each row from the schema data frame and populating the Pollution-Schema table
    for i,row in schema.iterrows():
        SQL_Cursor.execute(Populate_Schema_Query, tuple(row))
    Initialisation_key.commit() # Committing updates to the Pollution-Schema table
except Error as err:
    print("Error populating Pollution-Schema table: ", err)
    sys.exit()
else:
    print("Schema table is populated with required values")

print("--- %s seconds ---" % (time.time() - start_time)) 

print("--- %s seconds ---" % (time.time() - Start_Time_Main)) 