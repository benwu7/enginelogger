# read raw log from serial port and save the field in csv file for Grafana to display

import serial
from datetime import datetime
import os

########### testing ###########
from time import sleep
import random
########### testing ###########

def format_record(record):
    record_list = record.split(',')
    fields_pos = [
                3,4, #CHT 1, EGT 1
                5,6, #CHT 2, EGT 2
                7,8, #CHT 3, EGT 3
                9,10, #CHT 4, EGT 4
                11,12, #CHT 5, EGT 5
                13,14, #CHT 6, EGT 6
                ]
    ts_string = datetime.utcnow().isoformat()
    data = [str(int(record_list[i])) for i in fields_pos]
    output_list = [ts_string] + data
    return ",".join(output_list)

def main():

    _file_path = '/home/pi/playground/engine_data.csv'
    _rawlog_path = '/home/pi/playground/rawlog.csv'
    _archive_path = '/home/pi/playground/archive/'

    if os.path.exists(_file_path):
        os.rename(_file_path, _archive_path+datetime.utcnow().replace(microsecond=0).isoformat()+'.csv')

    with serial.Serial(port='/dev/ttyUSB0', baudrate=9600) as ser:
        while True:
            line = ser.readline()
            str_line = line.decode('ascii')

            with open(_rawlog_path, 'a') as mycsvfile:
                mycsvfile.write(datetime.utcnow().isoformat() + ',' + str_line + '\n')
            
            if str_line[0:4] == 'BBDR':
                output_string = format_record(str_line)
                if not os.path.exists(_file_path):
                    with open(_file_path, 'w') as mycsvfile:
                        mycsvfile.write('time,EGT1,CHT1,EGT2,CHT2,EGT3,CHT3,EGT4,CHT4,EGT5,CHT5,EGT6,CHT6' + '\n')
                with open(_file_path, 'a') as mycsvfile:
                    mycsvfile.write((output_string + '\n').strip('\x00'))
                    print(output_string)
            ########### testing ###########
            # line = "BBDR,OFF,UBG,382,1380,376,1400,390,1390,387,1387,369,1399,376,1459,0,0,0,0"
            # line = "BBDR,OFF,UBG," + ','.join([str(random.randint(200,450))+','+str(random.randint(1000,1600)) for i in range(8)])
            ########### testing ###########

            # output_string = format_record(line)
            # print(output_string)

            ########### testing ###########
            # sleep(5)
            ########### testing ###########

if __name__ == "__main__":
    main()
