from datetime import datetime
start = datetime.now()
import sys

# Defining prerequisites
source_filename = "crop.csv"
target_filename = "clean.csv"
source_delimiter = ";"
target_delimiter = ";"

# Creating a nested list of SiteID and Location pairs
Sid_Loc_pairs = [['188','AURN Bristol Centre'],['203','Brislington Depot'],['206','Rupert Street'],['209','IKEA M32'],
['213','Old Market'],['215','Parson Street School'],['228','Temple Meads Station'],['270','Wells Road'],
['271','Trailer Portway P&R'],['375','Newfoundland Road Police Station'],['395',"Shiner's Garage"],['452','AURN St Pauls'],
['447','Bath Road'],['459','Cheltenham Road \ Station Road'],['463','Fishponds Road'],['481','CREATE Centre Roof'],
['500','Temple Way'],['501','Colston Avenue'],['672','Marlborough Street']]

try:
    with open(source_filename, "r") as file: # Open the input file
        lines = file.readlines()
except FileNotFoundError as err:
    print("No such file exists in the target directory: {}".format(source_filename),"\nPlease check the file name or make sure it exists the the target directory")
    print(err)
    sys.exit()

print("The following lines are being removed either due a missing entry in SiteID field or due to a mismatch in SiteID and Location pairs")
print("\x1B[3m" + "Note: Header row is also included in the line count" + "\x1B[0m") 

try:
    file = open(target_filename,"w") # Create / Open the target file to write the cleaned data
except PermissionError as err:
    print("Unable to write to the target directory: {}".format(target_filename),"\nPlease check the file has write access if it already exists")
    print(err)
    sys.exit()


# Writing a function to perform string processing to split the desired columns are rearrange the new columns in a desired sequence
def words_split(words, key, key_loc, header=False):
    # Add header = True input to distinguish between header and data
    if header: # String processing for the header fields
        # Splitting "Date Time" into Date, Time and Time Offset fields
        if key == "Date Time":
            words.pop(key_loc)
            words.insert(key_loc, "Date")
            words.insert(key_loc+1, "Time")
            words.insert(key_loc+2, "Time Offset")
        # Splitting "geo_point_2d" into Latitude and Longitude
        elif key == "geo_point_2d":
            words.pop(key_loc)
            words.insert(key_loc,"Latitude")
            words.insert(key_loc+1,"Longitude")
        # Splitting "DateStart" into Date Start, Time Start and Time Start Offset fields
        elif key == "DateStart":
            words.pop(key_loc) 
            words.insert(key_loc, "Date Start")
            words.insert(key_loc+1, "Time Start")
            words.insert(key_loc+2, "Time Start Offset")
        # Splitting "DateEnd" into Date End, Time End and Time End Offset fields
        elif key == "DateEnd":
            words.pop(key_loc)
            words.insert(key_loc, "Date End")
            words.insert(key_loc+1, "Time End")
            words.insert(key_loc+2, "Time End Offset")
    else: # String processing for the data fields
        # Splitting "Date Time" into Date, Time and Time Offset fields
        if key == "Date Time": 
            date_time = words.pop(key_loc)
            if date_time == "": # Checking if Date Time field is a null
                words.insert(key_loc, "")
                words.insert(key_loc+1, "")
                words.insert(key_loc+2, "")
            else:
                date_time = date_time.split("T")
                date_split = date_time[0]
                time_offset = date_time[1]
                time_offset = time_offset.split("+")
                time_split = time_offset[0]
                offset_split = time_offset[1]
                words.insert(key_loc, date_split)
                words.insert(key_loc+1, time_split)
                words.insert(key_loc+2, offset_split)
        # Splitting "geo_point_2d" into Latitude and Longitude
        elif key == "geo_point_2d":
            geo_point = words.pop(key_loc)
            if geo_point == "": # Checking if geo_point_2d field is a null
                words.insert(key_loc, "")
                words.insert(key_loc+1, "")
            else:                           
                geo_point = geo_point.split(",")
                words.insert(key_loc, geo_point[0])
                words.insert(key_loc+1, geo_point[1])   
        # Splitting "DateStart" into Date Start, Time Start and Time Start Offset fields
        elif key == "DateStart":
            date_time_start = words.pop(key_loc)
            if date_time_start == "": # Checking if DateStart field is a null
                words.insert(key_loc, "")
                words.insert(key_loc+1, "")
                words.insert(key_loc+2, "")
            else:
                date_time_start = date_time_start.split("T")
                date_start_split = date_time_start[0]
                time_offset_start = date_time_start[1]
                time_offset_start = time_offset_start.split("+")
                time_start_split = time_offset_start[0]
                offset_start_split = time_offset_start[1]
                words.insert(key_loc, date_start_split)
                words.insert(key_loc+1, time_start_split)
                words.insert(key_loc+2, offset_start_split)
        # Splitting "DateEnd" into Date End, Time End and Time End Offset fields
        elif key == "DateEnd":
            date_time_end = words.pop(key_loc)
            if date_time_end == "": # Checking if Date End field is a null
                words.insert(key_loc, "")
                words.insert(key_loc+1, "")
                words.insert(key_loc+2, "")
            else:
                date_time_end = date_time_end.split("T")
                date_end_split = date_time_end[0]
                time_offset_end = date_time_end[1]
                time_offset_end = time_offset_end.split("+")
                time_end_split = time_offset_end[0]
                offset_end_split = time_offset_end[1]
                words.insert(key_loc, date_end_split)
                words.insert(key_loc+1, time_end_split)
                words.insert(key_loc+2, offset_end_split)
    return words

row_count = 0
for line in lines:
    words = line.split(source_delimiter)
    # This chunk of code can be simplified since the sequence and the indexes of the column name positions are known
    # Considering the low impact on the processing time, this code is written in an attempt to make the script more generic
    if row_count == 0:
        # The order in which key names are entered is not critical as they are reodedred later in the code
        keys = ['SiteID', 'Location', 'geo_point_2d', 'Date Time', 'DateStart', 'DateEnd']
        date_time_loc = words.index("Date Time")
        Location_loc = words.index("Location")
        SiteID_loc = words.index("SiteID")
        geo_point_loc = words.index("geo_point_2d")
        DateStart_loc = words.index("DateStart")
        DateEnd_loc = words.index("DateEnd")
        # Sequence of key_index values must match the sequnence in which keys are provided earlier
        key_index = [SiteID_loc, Location_loc, geo_point_loc, date_time_loc, DateStart_loc, DateEnd_loc]
        keys_sorted_zip = sorted(zip(key_index, keys))
        keys_sorted = [i for _, i in keys_sorted_zip]
        keys_index_sorted = sorted(key_index)

        for i in range(len(keys)-1,-1,-1): # Running the loop backwards to retain the previously calculated column numbers after each split
            key = keys_sorted[i]
            key_loc = keys_index_sorted[i]
            words_split(words, key, key_loc, header=True) # Splitting and rearanging column names
        line = target_delimiter.join(words) # Reformatting the line to csv format using the target delimiter
        file.write(line) # writing the line to the target file
        row_count += 2
    else:
        if words[SiteID_loc] == "": # Identifing and removing entries with missing Site_ID values
            print("SiteID value is MISSING in line {}".format(row_count))
            row_count += 1
        elif [words[SiteID_loc], words[Location_loc]] not in Sid_Loc_pairs: # Identifing and removing entries with mismatched SiteID and Location pairs
            print("SiteID and Location Name pair mismatch in line {Line_Number}".format(Line_Number = row_count))
            row_count += 1
        else: 
            for i in range(len(keys)-1,-1,-1):
                key = keys_sorted[i]
                key_loc = keys_index_sorted[i]
                words_split(words, key, key_loc) # Splitting and rearranging the data fields
            line = target_delimiter.join(words) # Reformatting the line to csv format using the target delimiter
            file.write(line) # writing the line to the target file
            row_count += 1
file.close()
print(datetime.now() - start)


        

