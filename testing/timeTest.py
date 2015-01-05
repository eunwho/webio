# Imports
import time
import datetime

start = time.time()

dataFileName = 'recording-'
dataFileName += datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
dataFileName += ".txt"

dataFileLineNumber = 0;
powerMeterData = "testData"

with open(dataFileName,'w') as fout:
    fout.write("Power Meter Monitoring System Data Log"+'\r'+'\n')

with open(dataFileName,'a') as fout:
    fout.write("======================================"+'\r'+'\n')

f_startTime = time.time()

def main():
    global start
    global dataFileLineNumber
    global dataFileName
    
    loopctrl = 1
    while loopctrl:
        end = time.time()
        f_elapsedTime = end - f_startTime
        if f_elapsedTime > 10.0 :
            f_startTime = time.time()

            dataFileLineNumber += 1
            s= str(dataFileLineNumber)+'\t'
        
            try:
                #dataFileName ="test.log"
                with open(dataFileName,'a') as files:
                    files.write(s)
                break
            except:
                dataFileName = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")+".txt"
                with open(dataFileName,'w') as fout:
                    fout.write("Power Meter Monitoring System Data Log"+'\r'+'\n')

                with open(dataFileName,'a') as fout:
                    fout.write("======================================"+'\r'+'\n')

                with open(dataFileName,'a') as f:
                    f.write(s)

            s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"+'\t'
            with open(dataFileName,'a') as f_opened:
                f_opened.write(s)

            powerMeterData = "Test string"
            s = powerMeterData +'\r'+'\n'
            with open(dataFileName,'a') as f_opened
                f_opened.write(s)
       
            
if __name__ == "__main__":
    main()
