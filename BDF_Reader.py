# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:11:05 2024

@author: press
"""
import numpy as np
import numpy.matlib

# This function extracts the eeg data from the Biosemi binary file
# and convert them into mat format. There are 20 fields, as decsribed in https://www.biosemi.com/faq/file_format.htm
# Despite the BDF format allows for saving different characteristics for each channel (e.g. different sampling frequencies, etc.)
# This code has been written under the assumption that all the channels will have the same characteristics (e.g. same sampling frequency, same gain, same filtering, etc.)
# See these links for a description of the BDF (https://www.biosemi.com/faq/file_format.htm)
# and EDF (https://edfrw.readthedocs.io/en/latest/specifications.html) format

#Biosemi range: 524 mV (-262,144 to +262,143 µV) (http://psychophysiology.cpmc.columbia.edu/Software/PolyRex/faq.html)

# Description of the BDF Header:	
#1) 8 bytes	Byte 1: "255" (non ascii)	Byte 1: "0" (ASCII)	Identification code

#1) 8 bytes: Bytes 2-8 : "BIOSEMI" (ASCII)	

#2) 80 bytes	User text input (ASCII) Local subject identification

#3) 80 bytes	 User text input (ASCII) Local recording identification

#4) 8 bytes	 dd.mm.yy (ASCII) Startdate of recording

#5) 8 bytes hh.mm.ss (ASCII) Starttime of recording

#6) 8 bytes (ASCII) Number of bytes in header record

#7) 44 bytes	"24BIT" (ASCII) Version of data format.

#8) 8 bytes (ASCII) Number of data records "-1" if unknown

#9) 8 bytes e.g.: "1" (ASCII) Duration of a data record, in seconds

#10) 4 bytes e.g.: "257" or "128" (ASCII) Number of channels (N) in data record

#11) N x 16 bytes e.g.: "Fp1", "Fpz", "Fp2", etc (ASCII) Labels of the channels

#12) N x 80 bytes e.g.: "active electrode", "respiration belt" (ASCII) Transducer type

#13) N x 8 bytes	e.g.: "uV", "Ohm" (ASCII) Physical dimension of channels

#14) N x 8 bytes	e.g.: "-262144" (ASCII)	Physical minimum in units of physical dimension

#15) N x 8 bytes	e.g.: "262143" (ASCII)	Physical maximum in units of physical dimension

#16) N x 8 bytes	e.g.: "-8388608" (ASCII)	e.g.: "-32768" (ASCII)	Digital minimum

#17) N x 8 bytes	e.g.: "8388607" (ASCII)	e.g.: "32767" (ASCII)	Digital maximum

#18) N x 80 bytes	e.g.: "HP:DC; LP:410"	e.g.: "HP:0,16; LP:500"	Prefiltering

#19) N x 8 bytes	For example: "2048" (ASCII) Number of samples in each data record (Sample-rate if Duration of data record = "1")

#20) N x 32 bytes	(ASCII) Reserved

#EEG is the structure used to save all the information extracted from the bdf data
class EEG_Class:
    
    pass

def extract_data_biosemi(BDF_file_selected,reference_channel):
    EEG = EEG_Class();
    
    bdf_file = open(BDF_file_selected, mode = "rb")
       
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
#Reading the information from the header file
    
    #Step 1
    #Read the first 8 bytes (all ASCII but the first byte)
    step_1 =  bdf_file.read(8)
    EEG_byte_1 = step_1[0];
    EEG_byte_1_2 = step_1[1:len(step_1)];
    EEG.byte_1 = [EEG_byte_1,EEG_byte_1_2.decode()];
    
    #Step 2
    #Read 80 bytes (ASCII)
    step_2 = bdf_file.read(80);
    EEG.byte_2 = step_2.decode();
    
    #Step 3
    #Read 80 bytes (ASCII)
    step_3 = bdf_file.read(80);
    EEG.byte_3 = step_3.decode();
 
    #Step 4
    #Read 8 bytes (ASCII)
    step_4 = bdf_file.read(8);
    EEG.byte_4 = step_4.decode();
 
    #Step 5
    #Read 8 bytes (ASCII)
    step_5 = bdf_file.read(8);
    EEG.byte_5 = step_5.decode();
 
    #Step 6
    #Read 8 bytes (ASCII)
    step_6 = bdf_file.read(8);
    EEG.byte_6 = step_6.decode();
 
    #Step 7
    #Read 44 bytes (ASCII)
    step_7 = bdf_file.read(44);
    EEG.byte_7 = step_7.decode();
 
    #Step 8
    #Read 8 bytes (ASCII)
    step_8 = bdf_file.read(8);
    EEG.byte_8 = step_8.decode();
 
    #Step 9
    #Read 8 bytes (ASCII)
    step_9 = bdf_file.read(8);
    EEG.byte_9 = step_9.decode();
    
    #Step 10
    #Read 4 bytes (ASCII)
    step_10 = bdf_file.read(4);
    EEG.byte_10 = step_10.decode();
    EEG.nbchan = int(EEG.byte_10);
    
    #Step 11
    #Read Nchannels*16 bytes (ASCII)
    step_11 = bdf_file.read(EEG.nbchan*16);
    EEG.byte_11 = step_11.decode();
    
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
 #Extract the labels of the channels recorded
    temp_chan = [];
    temp_chan = EEG.byte_11;
 
    start_count = 0;
    flag_count = 1;
    string_labels = EEG.byte_11;
    count_chars = 0;
    kk = 0;

    EEG.labels = [];    

    while (kk < EEG.nbchan - 1):
    
      while not(string_labels[count_chars] == ' '):
        
         if flag_count == 1:
            
           start_count = count_chars;  
           flag_count = 0;
         
         
         count_chars = count_chars + 1;
         
     
      if flag_count == 0 & kk < EEG.nbchan:  #The last channel is the status channel, which is the trigger, so it doesn't have to be included
               
          #count_chars = count_chars - 1;
          
          EEG.labels.append(temp_chan[start_count:count_chars]);
                                     
          flag_count = 1;
          
          kk = kk + 1;
          
     
      count_chars = count_chars + 1;

    #Step 12
    #Read Nchannels*80 bytes (ASCII)
    step_12 = bdf_file.read(EEG.nbchan*80);
    EEG.byte_12 = step_12.decode();

    #Step 13
    #Read Nchannels*8 bytes (ASCII)
    step_13 = bdf_file.read(EEG.nbchan*8);
    EEG.byte_13 = step_13.decode();
 
    #Step 14
    #Read Nchannels*8 bytes (ASCII)
    step_14 = bdf_file.read(EEG.nbchan*8);
    EEG.byte_14 = step_14.decode();
 
    #Step 15
    #Read Nchannels*8 bytes (ASCII)
    step_15 = bdf_file.read(EEG.nbchan*8);
    EEG.byte_15 = step_15.decode();
 
    #Step 16
    #Read Nchannels*8 bytes (ASCII)
    step_16 = bdf_file.read(EEG.nbchan*8);
    EEG.byte_16 = step_16.decode();
 
    #Step 17
    #Read Nchannels*8 bytes (ASCII)
    step_17 = bdf_file.read(EEG.nbchan*8);
    EEG.byte_17 = step_17.decode();
 
    max_physic_char = EEG.byte_15;

    track_index = [];
    max_physic = np.zeros((1,EEG.nbchan - 1));
    track_index_array = 0;
    previous_index = 0;
    
     
    for ll in range(len(max_physic_char)):
     
        if (max_physic_char[ll] == ' '):
         
             track_index.append(ll);
         
     
             if len(track_index) == 2 and track_index_array < EEG.nbchan:
                
                try:
                    max_physic[0,track_index_array] = float(max_physic_char[previous_index:track_index[0]]); 
                    previous_index = track_index[1] + 1;
                    track_index = [];
                    track_index_array = track_index_array + 1;
                    
                except:
                    previous_index = track_index[1] + 1;
                    track_index = [];
                    
                        
          
    min_physic_char = EEG.byte_14;
 
    track_index = [];
    min_physic = np.zeros((1,EEG.nbchan - 1));
    track_index_array = 0;
    previous_index = 0;
    
    for ll in range(len(min_physic_char)):
        
        if (min_physic_char[ll] == ' '):
         
             track_index.append(ll);
             
     
             if len(track_index) == 1 and track_index_array < EEG.nbchan:
                
                try:
                    min_physic[0,track_index_array] = float(min_physic_char[previous_index:track_index[0]]); 
                    previous_index = track_index[0] + 1;
                    track_index = [];
                    track_index_array = track_index_array + 1;
                    
                except:
                    previous_index = track_index[0] + 1;
                    track_index = [];
    
    max_dig_char = EEG.byte_17;

    track_index = [];
    max_dig = np.zeros((1,EEG.nbchan - 1));
    track_index_array = 0;
    previous_index = 0;
    
    for ll in range(len(max_dig_char)):
     
        if (max_dig_char[ll] == ' '):
         
            track_index.append(ll);
         
     
        if len(track_index) == 1 and track_index_array < EEG.nbchan - 1: 
         
            max_dig[0,track_index_array] = float(max_dig_char[previous_index:track_index[0]]);
            previous_index = track_index[0] + 1;
            track_index = [];
            track_index_array = track_index_array + 1;
     
    min_dig_char = EEG.byte_16;    

    track_index = [];
    min_dig = np.zeros((1,EEG.nbchan - 1));
    track_index_array = 0;
    previous_index = 0;
    
    for ll in range(len(min_dig_char)):
     
        if (min_dig_char[ll] == '-'):
         
            track_index.append(ll);
              
        if len(track_index) == 2 and track_index_array < EEG.nbchan - 1: 
         
            min_dig[0,track_index_array] = float(min_dig_char[track_index[0]:track_index[1]]);
            track_index.remove(track_index[0]);
            track_index_array = track_index_array + 1;   
            
    EEG.resolution = (max_physic - min_physic)/(max_dig - min_dig);

    #offset = max_physic - EEG.resolution*max_dig;
 
    #Step 18
    #Read Nchannels*80 bytes (ASCII)
    step_18 = bdf_file.read(EEG.nbchan*80);
    EEG.byte_18 = step_18.decode();
 
    #Step 19
    #Read Nchannels*8 bytes (ASCII)
    step_19 = bdf_file.read(EEG.nbchan*8);
    EEG.byte_19 = step_19.decode();
    sampl_freq_data_char = EEG.byte_19;
    
    track_index = [];
    for ll in range(len(sampl_freq_data_char)):
     
     if (sampl_freq_data_char[ll] == ' '):
         
         track_index.append(ll);
     
     if len(track_index) == 1:
         
         break;
    
    sampl_freq_data = float(sampl_freq_data_char[0:track_index[0]])/float(EEG.byte_9);
    
    EEG.srate = sampl_freq_data;
    EEG.pnts = EEG.srate*float(EEG.byte_8); 
 
    #Step 20
    #Read Nchannels*32 bytes (ASCII)
    step_20 = bdf_file.read(EEG.nbchan*32);
    EEG.byte_20 = step_20.decode();
    
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
#Starts reading the data. Move the pointer to the beginning of the first
#sample of each channel. Each sample is made of 24 bits (see Biosemi website),
# so we are reading in a group of 3 unsigned 8 bit integers
    EEG.data = np.zeros((EEG.nbchan-1,int(EEG.srate)*int(EEG.byte_8)));
    EEG.trigger_type = np.zeros((1,int(EEG.srate)*int(EEG.byte_8))) - 1;
    EEG.trigger_latency = np.zeros((1,int(EEG.srate)*int(EEG.byte_8))) - 1;
    EEG.trigger_status = np.zeros((1,int(EEG.srate)*int(EEG.byte_8))) - 1;
    
    for kk in range(1,EEG.nbchan + 1):
        
        bdf_file.seek((EEG.nbchan + 1)*256 + (kk - 1)*int(EEG.srate)*3, 0);
                    
        if kk == EEG.nbchan:    #This is the trigger channel
        
            track_trigger = 0;
        
            for ll in range(1,int(EEG.byte_8) + 1):
                temp_bytes = [];
                temp_bytes = bdf_file.read(int(sampl_freq_data)*3);
            
                trigger_type_lat_first8bits = temp_bytes[0:len(temp_bytes):3]; #These are the first 8 bits of the trigger line
                trigger_type_lat_second8bits = temp_bytes[1:len(temp_bytes):3]; #These are the second 8 bits of the trigger line
                trigger_type_lat_third8bits = temp_bytes[2:len(temp_bytes):3];  #These bits are used for the status of the trigger
        
                start_data = 0
                step_data = 3;
                track_sample = 0;
                 
                for mm in range(1,int(sampl_freq_data)):
                    
                    if mm > 1 or ll > 1:
                        
                     if((trigger_type_lat_first8bits[mm] != 0 or trigger_type_lat_second8bits[mm] != 0) and (trigger_type_lat_first8bits[mm] - trigger_type_lat_first8bits[mm-1] > 0) or (trigger_type_lat_second8bits[mm] - trigger_type_lat_second8bits[mm-1] > 0)):
                         EEG.trigger_type[0,track_trigger] = trigger_type_lat_first8bits[mm] + trigger_type_lat_second8bits[mm]*pow(2,8);
                         EEG.trigger_latency[0,track_trigger] = mm + (ll-1)*int(EEG.srate);
                         EEG.trigger_status[0,track_trigger] = bin(trigger_type_lat_third8bits[mm]).replace("0b", ""); #save the data in binary format;
                         
                         track_trigger += 1;
                     
                    else:
                     
                        if(trigger_type_lat_first8bits[mm] > 0 or trigger_type_lat_second8bits[mm] > 0):
                         EEG.trigger_type[0,track_trigger] = trigger_type_lat_first8bits[mm] + trigger_type_lat_second8bits[mm]*pow(2,8);
                         EEG.trigger_latency[0,track_trigger] = mm + (ll-1)*int(EEG.srate);
                         EEG.trigger_status[0,track_trigger] = bin(trigger_type_lat_third8bits[mm]).replace("0b", ""); #save the data in binary format;
                         
                         track_trigger += 1;
                     
                bdf_file.seek((EEG.nbchan + 1)*256 + (kk - 1)*int(EEG.srate)*3 + ll*EEG.nbchan*int(EEG.srate)*3, 0);
        
        else:
             #Since the duration of the data has been set to "1", we are reading 1 seconds of data at a time for each channel => 
             #=> (EEG.srate*3), because each sample is made of 3 bytes. Then skip the data for the remaining 
             #N -1 channels ((EEG.nbchan - 1)*EEG.srate*3), reads the next second of data, etc.    
             
             track_sample = 0;
             
             for ll in range(1,int(EEG.byte_8) + 1):
                 
                 temp_bytes = [];
                 temp_bytes = bdf_file.read(int(sampl_freq_data)*3);
                 
                 start_data = 0
                 step_data = 3;
                 
                 for mm in range(1,int(sampl_freq_data) + 1):
                     EEG.data[kk-1,track_sample] = temp_bytes[start_data] + temp_bytes[start_data + 1]*pow(2,8) + temp_bytes[start_data + 2]*pow(2,16);
                     EEG.data[kk-1,track_sample] = EEG.data[kk-1,track_sample] - pow(2,24)*(EEG.data[kk-1,track_sample] >= pow(2,23)); #Complement 2 conversion
                     EEG.data[kk-1,track_sample] = EEG.data[kk-1,track_sample]*EEG.resolution[0,kk-1];
                     start_data  += step_data;  
                     track_sample += 1;
                     
                 bdf_file.seek((EEG.nbchan + 1)*256 + (kk - 1)*int(EEG.srate)*3 + ll*EEG.nbchan*int(EEG.srate)*3, 0);
        
    #Remove the cells that have not been used in the trigger arrays
    size_array = EEG.trigger_type.shape;
    EEG.trigger_type = EEG.trigger_type[0,slice(-(size_array[1] - track_trigger))];
    EEG.trigger_latency = EEG.trigger_latency[0,slice(-(size_array[1] - track_trigger))]
    EEG.trigger_status = EEG.trigger_status[0,slice(-(size_array[1] - track_trigger))]
    
    # Rerefencing the data
    if (reference_channel == -1):
    
        EEG.data = -EEG.data;   #Used for the special module
    
    else:

        try:
        
            if(len(reference_channel) > 1):
                
                EEG.data = EEG.data - np.matlib.repmat(np.mean(EEG.data[reference_channel,0:int(EEG.srate)*int(EEG.byte_8)],0), (EEG.nbchan - 1) ,1);  #Rereference the data
                   
            else:
                
                EEG.data = EEG.data - np.matlib.repmat(EEG.data[reference_channel,0:int(EEG.srate)*int(EEG.byte_8)], (EEG.nbchan - 1) ,1);  #Rereference the data            
    
        except:
        
            print ('Re-referencing was not performed, because the channel(s) chosen were out of boundary');
            

    EEG.nbchan = EEG.nbchan - 1;

    bdf_file.close();  #close the binary file
    
    return EEG
