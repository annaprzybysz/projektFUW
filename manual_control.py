import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# input declaration
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# output declaration
GPIO.setup(18, GPIO.OUT, initial=1)

# printing the table
def print_table():
	print("----------------------------------------")
	print(" ")
	print("inputs    ", "in14 14        ", "in15 15        ")
	print("          ", GPIO.input(14), "             ", GPIO.input(15), "             ")
	print(" ")
	print("outputs   ", "in18 18[q]     ")
	print("          ", GPIO.input(18), "             ")
	print(" ")
	print("----------------------------------------")


print_table()
while True:
	temp = input("Read pins and change outputs")
	if temp == "ugabuga": 
		hehe = "xd"
	elif temp == "q":
		if GPIO.input(18) == False:
			GPIO.output(18, True)
		else:
			GPIO.output(18, False)
		print_table()
