#!/usr/bin/python
# -*- coding: utf-8 -*-

import Adafruit_MPR121.MPR121 as MPR121
import sys, os, time
from PySide import QtCore

import pygame  # for playing sounds only

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()


class touch_sensor(QtCore.QThread):
	
	dataEmit = QtCore.Signal(object)
	instrument = None
	lastInstrument = None
	
	music = None
	
	def run(self):
		print "Ο σένσορ άρχισε να λειτουργεί!\n"
		capSensor = MPR121.MPR121()
		if not capSensor.begin():
			print('Error initializing MPR121.  Check your wiring!')
			sys.exit(1)
		last_touched = capSensor.touched()
		self.music = instrumentDynamic()
		self.music.chooseInstrument("piano")  # Choose the instrument
		self.instrument = "piano"  # Set the local variable instrument for later use
		self.lastIntrument = "piano"  # Set the last instrument local variable in order to be able to change the instrument in the while loop
		while True:
			if self.lastInstrument != self.instrument:
				self.music.chooseInstrument(self.instrument)  # Select the instrument the user choose
				self.instrument = self.lastInstrument  # Update the instrument to be the last instrument
			current_touched = capSensor.touched()
			# Check each pin's last and current state to see if it was pressed or released.
			for i in range(12):
				# Each pin is represented by a bit in the touched value.  A value of 1
				# means the pin is being touched, and 0 means it is not being touched.
				pin_bit = 1 << i
				# First check if transitioned from not touched to touched.
				if current_touched & pin_bit and not last_touched & pin_bit:
					self.dataEmit.emit(i)
					#instrument.playsound(i)
					self.music.playsound(i)
			# Update last state and wait a short period before repeating.
			last_touched = current_touched
			time.sleep(0.1)
			
	@QtCore.Slot(str)
	def changeInstrument(self, instrument):
		print "Instrument changed in thread. Instrument selected: " + instrument
		self.instrument = instrument
		return
		
	@QtCore.Slot(int)
	def playNote(self, note):
		# Play a note requested via a signal
		self.music.playsound(note)
		return



class instrument():
	
	baseInstrumentFolder = "instruments/"  # Instrument files base folder
	instrument = [None]  # Current selected instrument
	instrumentKeys = [None] * 12  # Allocate a size 12 list for the key - sound bindings
	
	
	@staticmethod
	def chooseInstrument(instr):
		# Set the current selected instrument
		instrument.instrument = str(instr)
		instrument.updateInstrumentKeys()
		return
	
	@staticmethod
	def getInstrument():
		# Return the selected instrument
		return instrument.instrument
	
	@staticmethod	
	def updateInstrumentKeys():
		# Find all the files in the selected instrument foder and fill the list - sorted
		instrList = os.listdir(instrument.baseInstrumentFolder + instrument.instrument)
		instrList.sort()
		instrument.instrumentKeys = instrList
		return
		
	@staticmethod
	def playsound(sound):
		# sound argument should be an interger according to the key layout in the board
		# Play a sound that already exists in the instruments folder
		soundFile = instrument.baseInstrumentFolder + instrument.instrument + "/" + instrument.instrumentKeys[sound]
		playsound = pygame.mixer.Sound(soundFile).play()
		return
		

class instrumentDynamic():
	
	baseInstrumentFolder = "instruments/"  # Instrument files base folder
	instrument = None  # Current selected instrument
	instrumentKeys = [None] * 12  # Allocate a size 12 list for the key - sound bindings
	
	music_file = [None] * 12  # Preloaded music files!
	
	
	def chooseInstrument(self, instr):
		# Set the current selected instrument
		self.instrument = str(instr)
		self.updateInstrumentKeys()
		self.loadInstruments()
		return
		
	def loadInstruments(self):
		for x in range(0, len(self.music_file)):
			self.music_file[x] = pygame.mixer.Sound(self.baseInstrumentFolder + self.instrument + "/" + self.instrumentKeys[x])
		return
	
	
	def getInstrument(self):
		# Return the selected instrument
		return self.instrument
	
	
	def updateInstrumentKeys(self):
		# Find all the files in the selected instrument foder and fill the list - sorted
		instrList = os.listdir(self.baseInstrumentFolder + self.instrument)
		instrList.sort()
		self.instrumentKeys = instrList
		return
		
		
	def playsound(self, sound):
		# sound argument should be an interger according to the key layout in the board
		# Play a sound that already exists in the instruments folder
		#soundFile = self.baseInstrumentFolder + self.instrument + "/" + self.instrumentKeys[sound]
		#playsound = pygame.mixer.Sound(soundFile).play()
		self.music_file[sound].play()  # Preloaded sounds
		return
