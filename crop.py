from datetime import datetime
start = datetime.now()

import sys

# Writing a function to read the source file, remove entries with missing data time values and extract entries on or after 2010
def cropcsv(source_filename, target_filename, delimiter):
    try:
        with open(source_filename, "r") as source_file:
            lines = source_file.readlines()
    except FileNotFoundError as err:
        print("No such file exists in the target directory: {}".format(source_filename),"\nPlease check the file name or make sure it exists the the target directory")
        print(err)
        sys.exit()
    
    try:
        target_file = open(target_filename,"w")
    except OSError as err:
        print(err)
        sys.exit()
    line_count = 1
    lines_written_count = 0
    for line in lines:
        words = line.split(delimiter)  # Splitting lines using the specified delimiter
        if line_count == 1: # Identifying the header line writing it to the target file
            target_file.write(line)
            print("Header row is written to {}".format(target_filename))
            lines_written_count += 1
        elif words[0] == "": # Identifying missing Date Time entries and printing their line numbers to the console 
            print("missing datetime in line {C} of {F}".format(C=line_count, F=source_filename))
        else:
            if words[0] >= "2010-01-01T00:00:00+00:00": # Identifying and writing entries which are after 2010 to the target file
                target_file.write(line)
                lines_written_count += 1
        line_count += 1
    target_file.close()
    print(lines_written_count)            


filename_source = "air-quality-data-continuous.csv"
filename_target = "crop.csv"
delimiter = ";"
cropcsv(filename_source, filename_target, delimiter)          

print(datetime.now() - start)

        
