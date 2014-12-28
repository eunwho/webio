# Imports
import time

start = time.time()

def main():
    global start

    loopctrl = 1
    while loopctrl:
        end = time.time()
        elapsedTime = end - start
        if elapsedTime > 60.0 :
            start = time.time()
            print( " Elasped time = %d",elapsedTime)

            
if __name__ == "__main__":
    main()
