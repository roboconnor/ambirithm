#
# Ambirithm v1.0 (if you could even call it a version 1!)
#
# Created on 21/11/2019
# Written by Rob O'Connor
#
# Last modified on 09/12/2019

import os, random, subprocess, csv, datetime
from datetime import datetime

processes = [] #an array of processes, each of which will be an instance of omxplayer
x = 1 # keeps us in an infinite loop (for now)
log_file = '/home/pi/Desktop/ambirithm/ambirithm_log.csv'
soundpass = 0  #index of how many loops of sound players have run

while x == 1:
    soundpass = soundpass + 1

    soundbank = random.randint(1,10)
    print("Playing Sound Bank : ", soundbank)

    sound_dir = '/home/pi/Desktop/ambirithm/'+str(soundbank)
    pad_dir = sound_dir+'/4-Pad/'
    low_dir = sound_dir+'/3-Low/'
    mid_dir = sound_dir+'/2-Mid/'
    high_dir = sound_dir+'/1-High/'

    num_repeats = random.randint(1,1)
    #print("Num Repeats: ", num_repeats)

    for i in range(num_repeats):
        pad_file = random.choice(os.listdir(pad_dir))
        low_file = random.choice(os.listdir(low_dir))
        mid_file = random.choice(os.listdir(mid_dir))
        high_file = random.choice(os.listdir(high_dir))

        pad_path = pad_dir+pad_file
        low_path = low_dir+low_file
        mid_path = mid_dir+mid_file
        high_path = high_dir+high_file

        # Creating a bunch of processes to play audio simultaneously 
        omxp_pad = subprocess.Popen(['omxplayer', pad_path])
        omxp_low = subprocess.Popen(['omxplayer', low_path])
        omxp_mid = subprocess.Popen(['omxplayer', mid_path])
        omxp_high = subprocess.Popen(['omxplayer', high_path])

        # Adding all the processes to the array
        processes.append(omxp_pad)
        processes.append(omxp_low)
        processes.append(omxp_mid)
        processes.append(omxp_high)

        print("Selected Pad: ", pad_file)
        print("Selected Low: ", low_file)
        print("Selected Mid: ", mid_file)
        print("Selected High: ", high_file)

        # Writing soundpass info to the log file (CSV formatted)
        with open(log_file, mode='a') as log_file_handle:
            log_file_writer = csv.writer(log_file_handle, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            date_readable = datetime.fromtimestamp(timestamp)
            log_file_writer.writerow([date_readable,str(soundbank),pad_file,low_file,mid_file,high_file]) 
        
        # Check to see if all processes are running. 
        # When all processes have finished, it should bug out
        for p in processes:
                if p.wait() != 0:
                    print("Error")

        print("Finished Pass ", soundpass)

# EOF
        
