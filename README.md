# Biosemi-BDF-Reader-Python
Theis file reads Biosemi data in BDF format. Please, keep in mind that I am following the current format of the BDF file, as reported in Biosemi's website. This means that my code assumes that the data are read every 1 second. If the format changes and I am not aware of that, please contact me and I will make the appropriate changes. Since I have never worked with data different from EEG, I have not been able to test the code with other input, such as Ergo input.

BDF_Reader: This function takes two input: 1) the name of the BDF file to open and 2) the refernce channel(s) expressed in number (position). If more than one reference channel is used, the function will average the N channels entered. The function handles the special module 9 "ABR", which does not require a reference channel. In this case, the user needs to enter "-1". The polarity will also be adjusted to have Cz - Average channeles. The function will return one ouput (e.g. EEG), which stores all the key info data read from the bdf file, such as the EEG data, the sampling frequency, etc.

If you have any questions and/or want to report bugs, please e-mail me (Ale) at: pressalex@hotmail.com
