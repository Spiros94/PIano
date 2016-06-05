#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, time

class readLif():
	
	defaultLocation = "lifs/"  # Note the trailing slash!
	
	songs = []  # The list with the lif files including the extensions
	
	@staticmethod
	def openFiles():
		# Discovers all files in lifs folder and stores them into readLif.songs list with their extension
		for file in os.listdir(readLif.defaultLocation):
			readLif.songs.append(file)
		return
	
	@staticmethod		
	def getFileNames():
		# Returns a list with the filenames without the extension
		filenames = []
		for file in readLif.songs:
			filename, extension = os.path.splitext(file)
			filenames.append(filename)
		return filenames
		
	@staticmethod
	def getDifficulty(file):
		# Opens a lif file and extract the difficulty from it
		with open(readLif.defaultLocation + file + ".lif") as f:  # Opens the file name, reads the first line which represents the defficulty and return it
			for line in f:
				return line
				
	@staticmethod		
	def getInstrument(file):
		# Opens a lif file and extracts the instrument that the track should be played on
		with open(readLif.defaultLocation + file + ".lif") as f:
			for i, line in enumerate(f):
				if i == 1:
					return line
					
	@staticmethod
	def getTotalRows(file):
		# Get the total row number of the lif file
		with open(readLif.defaultLocation + file + ".lif") as f:
			for i, line in enumerate(f):
				pass
			return i+1
		return
	
	@staticmethod
	def getLines(file):
		# Returns a list containg in each row every line of the lif file
		lines = [line.rstrip('\n') for line in open(readLif.defaultLocation + file + ".lif")]
		return lines
