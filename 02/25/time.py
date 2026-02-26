import time

epc=time.time()
print(epc)
localtime=time.localtime(epc)
print (
    "Date:", localtime.tm_mon,"/",localtime.tm_mday, "/",localtime.tm_year, "      ", 
    "Time:", localtime.tm_hour, ":", localtime.tm_min, ":", localtime.tm_sec
    )

