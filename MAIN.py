from time import sleep    #minimum sleep time is 0.0001s (it gives about 0.0003s in reality)
from datetime import datetime    #datetime.now() gives a very precise time readout
import RPi.GPIO as GPIO   #imports Raspberry functions which will start with GPIO
GPIO.setmode(GPIO.BCM)    #it chooses the pin numbering system from the diagram
GPIO.setwarnings(False)   #sometimes useless warnings pop up
GPIO.setup(2, GPIO.OUT, initial=1)  #PL
GPIO.setup(3, GPIO.OUT, initial=0)  #SHCP
GPIO.setup(4, GPIO.OUT, initial=1)  #MR
GPIO.setup(17, GPIO.OUT, initial=1) #Trg debugger
GPIO.setup(24, GPIO.OUT, initial=1) #Trg block
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #1st Q - Data input
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #2nd Q - Data input
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #3rd Q - Data input
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #4th Q - Data input
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #STCP Trigger
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #debugger

#opens the main file in 'w' = 'write' mode
file = open('MAIN.txt', 'w')
file.write( 'program start: ' + str(datetime.now()) + '\n\n' )

#sets detection of the trigger in a way that can be used in a loop
#used in this way Ctrl+C will always stop the program immidiately
#(Ctrl+C is a stop command when using 'try:' and 'except:')
GPIO.add_event_detect(18, GPIO.RISING)

#main loop - wait for trigger -when it comes save data into lists and then into file
while True:
  # Reset of the lists with registered values
  register1 = []
  register2 = []
  register3 = []
  register4 = []

  # Step 1 - MR - reset of the shift register
  GPIO.output(4, False)
  sleep(0.0001)
  GPIO.output(4, True)

  # Step 2 - STCP - wait for trigger
  try:
    while True:
      sleep(0.01) #to not overwork the computer
      #if trigger detected get out of the loop and proceed with data readout
      if GPIO.event_detected(18):
        break
        
  # It gives the option to break the loop if you press Ctrl+C
  except:
    break

  # Write the trigger time to the file
  file.write( 'read start: ' + str(datetime.now()) + '\n' )

  # Block incoming triggers during data readout 
  GPIO.output(24, False)
  
  # Step 3 - PL - activate Parallel loading
  GPIO.output(2, False)
  sleep(0.0001)
  GPIO.output(2, True)

  # Step 4 - SHCP and Q - Reading data from Shift Register to Raspberry
  for i in range(8):
    # Saving Q to the lists
    register1.append(GPIO.input(14))
    register2.append(GPIO.input(15))
    register3.append(GPIO.input(17))
    register4.append(GPIO.input(27))

    # SHCP - 1 clock tick
    GPIO.output(3, True)
    sleep(0.0001)
    GPIO.output(3, False)

  # Write the 'finished reading' time to the file
  file.write( 'read stop:  ' + str(datetime.now()) + '\n' )

  # Writing data on the screen and to the file
  print (register1, " ", register2, " ", register3, " ", register4, " Press Ctrl+C to stop the program.\n")
  file.write( str(register1) + str(register2) + str(register3) + str(register4) + '\n\n' )

  GPIO.output(24, True)

# Write the program finish time to the file
file.write( 'program end: ' + str(datetime.now()) )

file.close()
