import os
from os.path import join
import configparser
import csv

CONF = 'iometer_csv_parser.ini'
cfg = configparser.ConfigParser()
cfg.read(CONF, 'utf8')
folders = cfg.get('Scan', 'ScanFolder').split(';')

result_dict = []
for folder in folders:
    test_name = os.path.basename(folder)  # extract Test Name from the folder name
    for (dirname, dirs, files) in os.walk(folder):
        for filename in files:
            if filename.endswith('csv'):
                vmname = filename.split(".")[0][8:]    # extract VM name from the file name
                csv_content = []
                for row in csv.reader(open(os.path.join(dirname, filename)), delimiter=",", skipinitialspace=True):    # put CSV content in a big list
                    csv_content.append(row)
                for element in csv_content:    # start parsing the content one by one
                    try:
                        if not element: #if the element is empty, skip it. 
                            continue
                        elif element[0] == "'Time Stamp":    #if the element starts with 'Time Stamp, the next element is the test time
                            time_stamp_position = csv_content.index(element)+1
                            time_stamp = csv_content[time_stamp_position][0]
                        elif element[0] == "'size":    #if the element starts with 'size, the next element will be test configurations
                            test_config_position = csv_content.index(element)+1
                            block_size = csv_content[test_config_position][0]
                            percent_reads = csv_content[test_config_position][2]
                            percent_random = csv_content[test_config_position][3]
                        elif element[0] == "'Target Type":    #if the element starts with 'Target Type, the next element will be test result
                            test_result_position = csv_content.index(element)+1
                            IOps = csv_content[test_result_position][6]
                            MBps = csv_content[test_result_position][9]
                            AvgRespTime = csv_content[test_result_position][14]
                            MaxRespTime = csv_content[test_result_position][19]
                            percent_CPU = csv_content[test_result_position][45]
                    except:
                        print("not able to parse:")
                        print(element)
                        continue
                result = [test_name, vmname, time_stamp, block_size, percent_reads, percent_random, IOps, MBps, AvgRespTime, MaxRespTime, percent_CPU]
                result_dict.append(result)

#print(result_dict)
print(len(result_dict))

ofile  = open('iometer_csv_parser.csv', "w", newline='')
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(["Test Name", "Guest VM Name", "Time Stamp", "Transfer Request Size", "Percent Read/Write Distribution", "Percent Random/Sequential Distribution", "Total I/O per Second", "Total MBs per Second", "Average I/O Response Time (ms)", "Maximum I/O Response Time (ms)", "CPU Utilization (total)"])
writer.writerows(result_dict)
ofile.close()
