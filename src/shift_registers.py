import RPi.GPIO as GPIO
from PySide import QtCore

GPIO.setmode(GPIO.BCM)  # set the mode of the Raspberry PI pins to BCM
LATCH_PIN = 17  # The pin 12 on the chip
CLOCK_PIN = 18  # The pin 11 on the chip
DATA_PIN = 4    # The pin 14 on the chip
OUTPUT_ENABLED_PIN = 27  # Pin 13 on the chip

GPIO.setwarnings(False)
GPIO.setup(LATCH_PIN, GPIO.OUT)
GPIO.setup(CLOCK_PIN, GPIO.OUT)
GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(OUTPUT_ENABLED_PIN, GPIO.OUT)
GPIO.setwarnings(True)

class shiftRegister(QtCore.QObject):

    @staticmethod
    def writeSR(value):
        # Make sure all the clocks are initiated
        GPIO.output(OUTPUT_ENABLED_PIN, 0)
        GPIO.output(CLOCK_PIN, 0)
        GPIO.output(LATCH_PIN, 0)
        valuetmp = value
        for x in range(0,8):
            temp = valuetmp & 0x80  # Take the value of the MSB
            if temp == 0x80:      # Check the MSB value and if 1 - output 1 to the data pin
                GPIO.output(DATA_PIN, 1)
            else:
                GPIO.output(DATA_PIN, 0) 
            shiftRegister.pulseClock()  # Store the data into the shift register in one clock period
            valuetmp = valuetmp << 0x01 # shift left by one to check the next digit
        shiftRegister.pulseLatch() # Output the value to the pins on the shift register
        return
        

    @staticmethod
    def writeSRL(list,reverse=False):
        # This function takes a list and a boolean(optional) parameter. If the reverse-boolean parameter is True then the passed list is reversed
        if reverse:
            list = list[::-1]
        GPIO.output(OUTPUT_ENABLED_PIN, 0)
        GPIO.output(CLOCK_PIN, 0)
        GPIO.output(LATCH_PIN, 0)
        for x in range(0, len(list)):
            if list[x] == 1:
                GPIO.output(DATA_PIN, 1)
            else:
                GPIO.output(DATA_PIN, 0)
            shiftRegister.pulseClock()
        shiftRegister.pulseLatch()
        return


    @staticmethod
    def pulseClock():
        GPIO.output(CLOCK_PIN, 1)
        GPIO.output(CLOCK_PIN, 0)
        return
    
    
    @staticmethod
    def pulseLatch():
        GPIO.output(LATCH_PIN, 1)
        GPIO.output(LATCH_PIN, 0)
        return


    @staticmethod
    def clearAll():
		# Clear all the leds from the shift registers by passing zeros to all of them
        for x in range(0,5):
            shiftRegister.writeSR(0b00000000)


    @staticmethod
    def testLeds():
        '''
        Tests made about the shift registers
        led_list = [0,0,1,0,0,1,0,1]
        shiftRegister.writeSRL(led_list)
        led_list = [0,0,1,0,0,1,0,1]
        shiftRegister.writeSRL(led_list)
        led_list = [0,0,1,0,0,1,0,1]
        shiftRegister.writeSRL(led_list)
        led_list = [0,0,1,0,0,1,0,1]
        shiftRegister.writeSRL(led_list)
        led_list = [0,0,1,0,0,1,0,1]
        shiftRegister.writeSRL(led_list)
        '''
        led_list = [None] * 40   # Make an empty list for the led status
        for x in range (0, 40):  # Zero out the list
            led_list[x] = 0

        for x in range(0, 40):  # Light up a led and turn off the previous one - if exists
            led_list[x] = 1
            led_list[x-1] = 0
            shiftRegister.writeSRL(led_list)
            time.sleep(0.1)
            
        shiftRegister.clearAll()
        time.sleep(0.5)
        for x in range(0, 40):  # Fill the list to test the leds all together
            led_list[x] = 1
        
        shiftRegister.writeSRL(led_list)
        time.sleep(0.5)
        shiftRegister.clearAll()
        
TELO3_LEDS = [2,3,4,5,8,9,10,11,12,13,14,15,17,18,19,23,24,25,27,28,29,30,32,33,34,35]
TELO3_LEDS1 = [0,1,2,4,7,9,10,11,12,13,15,16,17,19,21,23,24,26,27,28,29,30,32,33,34,35]
