#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import time, sys
import threading
import os

execfile("shift_registers.py")  # Import the shift registers code from other file
execfile("touch_sound.py")  # MPR121 sensor/sounds
execfile("read_lifs.py")

class Ui_MainWindow(QtCore.QObject):
	proponisi_mode = False
	
	lastTouched = -1  # -1 for nothing pressed - get's the value from the MPR121 with signal
	playingSong = False
	
	changeInstrumentSignal = QtCore.Signal(object)
	playNote = QtCore.Signal(object)
	
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setWindowModality(QtCore.Qt.NonModal)
		MainWindow.resize(483, 304)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("piano.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		self.centralWidget = QtGui.QWidget(MainWindow)
		self.centralWidget.setObjectName("centralWidget")
		self.tableWidget = QtGui.QTableWidget(self.centralWidget)
		self.tableWidget.setGeometry(QtCore.QRect(10, 40, 461, 161))
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(0)
		item = QtGui.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem()
		self.tableWidget.setHorizontalHeaderItem(2, item)
		self.label = QtGui.QLabel(self.centralWidget)
		self.label.setGeometry(QtCore.QRect(10, 10, 161, 21))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setWeight(75)
		font.setBold(True)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.pushButton = QtGui.QPushButton(self.centralWidget)
		self.pushButton.setGeometry(QtCore.QRect(370, 220, 101, 31))
		self.pushButton.setObjectName("pushButton")
		self.checkBox = QtGui.QCheckBox(self.centralWidget)
		self.checkBox.setGeometry(QtCore.QRect(220,220,140,31))
		self.checkBox.setObjectName("checkBox")
		self.doubleSpinBox = QtGui.QDoubleSpinBox(self.centralWidget)
		self.doubleSpinBox.setGeometry(QtCore.QRect(30,225,80, 30))
		self.doubleSpinBox.setSingleStep(0.15)
		self.doubleSpinBox.setObjectName("doubleSpinBox")
		self.label1 = QtGui.QLabel(self.centralWidget)
		self.label1.setGeometry(QtCore.QRect(10, 200,140, 30))
		self.label1.setObjectName("label1")
		MainWindow.setCentralWidget(self.centralWidget)
		self.menuBar = QtGui.QMenuBar(MainWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 483, 21))
		self.menuBar.setObjectName("menuBar")
		self.menuFile = QtGui.QMenu(self.menuBar)
		self.menuFile.setObjectName("menuFile")
		self.menuAbout = QtGui.QMenu(self.menuBar)
		self.menuAbout.setObjectName("menuAbout")
		self.menu = QtGui.QMenu(self.menuBar)
		self.menu.setObjectName("menu")
		MainWindow.setMenuBar(self.menuBar)
		self.statusBar = QtGui.QStatusBar(MainWindow)
		self.statusBar.setObjectName("statusBar")
		MainWindow.setStatusBar(self.statusBar)
		self.actionExit = QtGui.QAction(MainWindow)
		self.actionExit.setObjectName("actionExit")
		self.action = QtGui.QAction(MainWindow)
		self.action.setObjectName("action")
		self.action_2 = QtGui.QAction(MainWindow)
		self.action_2.setObjectName("action_2")
		self.actionLed_Test = QtGui.QAction(MainWindow)
		self.actionLed_Test.setObjectName("actionLed_Test")
		self.actionAbout = QtGui.QAction(MainWindow)
		self.actionAbout.setObjectName("actionAbout")
		self.menuFile.addAction(self.actionExit)
		self.menuAbout.addAction(self.actionAbout)
		self.menu.addAction(self.action)
		self.menu.addAction(self.action_2)
		self.menu.addAction(self.actionLed_Test)
		self.menuBar.addAction(self.menuFile.menuAction())
		self.menuBar.addAction(self.menu.menuAction())
		self.menuBar.addAction(self.menuAbout.menuAction())
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)  # Align table headers to the middle
		self.action_2.setCheckable(True)
		
		# connect the button actions to the functions made
		ui.actionAbout.triggered.connect(self.aboutDialogMsg)  # Connect the About Dialog with the Help->About menu button
		ui.actionExit.triggered.connect(self.exitApp)  # Connect the File->Exit menu button with the self.exitApp function
		ui.actionLed_Test.triggered.connect(self.ledTest)  # Connect the "Επιλογές"-> Led Test with the self.ledTest function
		ui.action.triggered.connect(self.chooseInstrumentA)  # Connect the "Επιλογές"-> "Επιλογή οργάνου" with the self.chooseInstrumentA function
		ui.action_2.triggered.connect(self.setProponisi)
		ui.pushButton.clicked.connect(self.playSong)
		
		
		#test code for shift registers
		shiftRegister.clearAll()  # Make sure all leds are turned off first
		#shiftRegister.testLeds()
		self.sensor = touch_sensor()  # Initiate the capacitive sensor
		self.sensor.dataEmit.connect(self.printEmited)  # Connect the sensor to the printEmited function mainly for training mode
		self.playNote.connect(self.sensor.playNote) # Connect the local note playing singal with the threaded instrument/sensor
		self.changeInstrumentSignal.connect(self.sensor.changeInstrument)
		self.sensor.start()  # Start running the capacitive sensor as it is in another thread for non blocking gui function
		self.changeInstrumentSignal.emit("piano")  # Emit a signal for changing the instrument in the thread
		
		
		instrument.chooseInstrument("piano")  # Set piano as the default instrument
		lis = [0]*40
		for x in TELO3_LEDS1:
			lis[x] = 1
		shiftRegister.writeSRL(lis, True)
		readLif.openFiles()  # Read the lif files from the folder
		
		for name in readLif.getFileNames(): # Get all the file names and iterate through them
			rowCount = ui.tableWidget.rowCount()  # Get the current row in order to append after it one more row
			ui.tableWidget.insertRow(rowCount)  # Append after the last row, a new one
			ui.tableWidget.setItem(rowCount, 0, QtGui.QTableWidgetItem(name))  # Set the name in the first column
			ui.tableWidget.setItem(rowCount, 1, QtGui.QTableWidgetItem(readLif.getDifficulty(name)))  # The second column in the row contains the difficulty
			ui.tableWidget.setItem(rowCount, 2, QtGui.QTableWidgetItem(readLif.getInstrument(name)))  # The third column contains the instrument the lif should be played on
		return # Setup UI

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PIano Project 2016", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Τίτλος Τραγουδιού", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Δυσκολία", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Όργανο", None, QtGui.QApplication.UnicodeUTF8))
		self.label.setText(QtGui.QApplication.translate("MainWindow", "Λίστα τραγουδιών:", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Παίξε!", None, QtGui.QApplication.UnicodeUTF8))
		self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "Αρχείο", None, QtGui.QApplication.UnicodeUTF8))
		self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
		self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "Επιλογές", None, QtGui.QApplication.UnicodeUTF8))
		self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Έξοδος", None, QtGui.QApplication.UnicodeUTF8))
		self.action.setText(QtGui.QApplication.translate("MainWindow", "Επιλογή Οργάνου", None, QtGui.QApplication.UnicodeUTF8))
		self.action_2.setText(QtGui.QApplication.translate("MainWindow", "Προπόνηση Mode", None, QtGui.QApplication.UnicodeUTF8))
		self.actionLed_Test.setText(QtGui.QApplication.translate("MainWindow", "Led Test", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
		self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Επίδειξη Κομματιού", None, QtGui.QApplication.UnicodeUTF8))
		self.label1.setText(QtGui.QApplication.translate("MainWindow", "Επιτάχυνση Τραγουδιού:", None, QtGui.QApplication.UnicodeUTF8))
		return

	def aboutDialogMsg(QObject):
		msg = QtGui.QMessageBox()  # Create a new message box to show the names of the creators of the project
		msg.setWindowTitle("About") # Set the title
		msg.setText(u"Project για τα Τέλο 3 - 2016<br \> Σαμαράς Τάσος - Project Manager<br \>Αγγελίδης Αλέξανδρος<br \> Βασιλειάδης Κώστας<br \>Ηλιάδης Νίκος<br \>Κρασογιάννης Σταύρος<br \> Μητρόπουλος Σπύρος<br \>Μπουριτζής Σάκης<br \>")
		msg.exec_()  # Show the message box in the screen
		return
		

	def ledTest(self):
		# User pressed on the Led Test button on the menu
		t1 = threading.Thread(target=shiftRegister.testLeds)  # Start the test in a new thread
		t1.start()
		msg = QtGui.QMessageBox.information(None, u"Τεστ σε εξέλιξη", u"Το τεστ γίνεται αυτή τη στιγμή. Πατήστε ΟΚ και περιμένετε για το μήνυμα ολοκλήρωσης") # Inform the user about the led test
		t1.join()   # Wait until thread completes the test and then call the testComplete function
		self.testComplete()
		return

	def testComplete(self):
		# When the led test completes this message will show up
		msg = QtGui.QMessageBox()
		msg.setWindowTitle(u"Επιτυχία!")
		msg.setText(u"Το τέστ ολοκληρώθηκε με επιτυχία!")
		msg.exec_()
		return

	def chooseInstrumentA(self):
		# When the choose instrument key from the menu is pressed the user will be prommpted to select for an instrument from the instruments folder
		instrumentList = os.listdir(instrument.baseInstrumentFolder)  # List the folder of instruments to let the user select based on the name of the folder
		choice, answer = QtGui.QInputDialog.getItem(None, u"Επιλογή Οργάνου", u"Επιλέξτε όργανο από τη λίστα παρακάτω", instrumentList, 0, False)  # PopUp the question box
		if answer == True:  # If the user pressed the "OK" button
			#instrument.chooseInstrument(choice)
			self.changeInstrumentSignal.emit(choice)
		return
		
	def printEmited(self, data):
		# Get the signal asynchronously from the MPR121 thread for lighting up the led and play the sound - if it is in proponisi mode
		if self.proponisi_mode:
			led_list = [0]*40
			led_list[data*3] = 1
			shiftRegister.writeSRL(led_list, True)
		return
		
	def setProponisi(self):
		# When the action for training is pressed - trigger the action
		if self.proponisi_mode == True:
			self.proponisi_mode = False
		else:
			self.proponisi_mode = True
		shiftRegister.clearAll()
		return
		
	def playSong(self):
		if len(ui.tableWidget.selectedItems()) < 1:  # Check if there is a selected song-row
			msg = QtGui.QMessageBox()
			msg.setWindowTitle(u"Επιλογή Τραγουδιού")
			msg.setText(u"Παρακαλώ επιλέξτε τραγούδι πρώτα και μετά πατήστε το πλήκτρο \"Παίξε!\"")
			msg.exec_()
			return
		filename = ""
		for item in ui.tableWidget.selectedItems():
			filename = ui.tableWidget.item(item.row(), 0).text()  # Get the filename from the table widget as user clicked in a row
			
		self.proponisi_mode = False  # Disable the traning mode if it is enabled
		self.action_2.setChecked(False) # Disable the check if existed
		
		shiftRegister.clearAll()  # Clear all leds to start playing the song
		MainWindow.setEnabled(False)
		self.playingSong = True
		msg = QtGui.QMessageBox()
		msg.setWindowTitle(u"Τραγούδι επιλέχθηκε")
		msg.setText(u"Το τραγούδι <strong>" + filename + u"</strong> έχει επιλεγεί. Όταν είστε έτοιμοι πατήστε το πλήκτρο OK")
		msg.exec_()
		time.sleep(1)
		
		totalLines = readLif.getTotalRows(filename)
		fileLines = readLif.getLines(filename)
		
		speedUp = self.doubleSpinBox.value()
		
		for x in range(2, totalLines-2):	# read the notes and the delays for them and iterate through them
			KeyToBePressed, DelayUntiPressed = fileLines[x].split(":", 2)  # For each note and the next two ones, take the delays and notes
			KeyToBePressed1, DelayUntiPressed1 = fileLines[x+1].split(":", 2)
			KeyToBePressed2, DelayUntiPressed2 = fileLines[x+2].split(":", 2)
			led_list = [0]*40   #  Make a list with all leds cleared
			led_list[int(KeyToBePressed)*3] = 1  # Blue leds, the leds should be played first
			led_list[int(KeyToBePressed1)*3+1] = 1  # Green leds for the next after blue 
			led_list[int(KeyToBePressed2)*3+2] = 1  # Red led last led comming
			if self.checkBox.isChecked() == True:
				self.playNote.emit(int(KeyToBePressed))
			shiftRegister.writeSRL(led_list, True)  # Write the list to the shift registers in reversed order
			time.sleep(float(DelayUntiPressed)*(1/speedUp))
			
		# Last two notes are out of range and should manually display the leds
		KeyToBePressed, DelayUntiPressed = fileLines[totalLines-2].split(":", 2)
		KeyToBePressed1, DelayUntiPressed1 = fileLines[totalLines-1].split(":", 2)
		led_list = [0]*40
		led_list[int(KeyToBePressed)*3] = 1
		led_list[int(KeyToBePressed1)*3+1] = 1
		self.playNote.emit(int(KeyToBePressed))
		shiftRegister.writeSRL(led_list, True)
		time.sleep(float(DelayUntiPressed)*(1/speedUp))
		
		KeyToBePressed, DelayUntiPressed = fileLines[totalLines-1].split(":", 2)
		led_list = [0]*40
		led_list[int(KeyToBePressed)*3] = 1
		self.playNote.emit(int(KeyToBePressed))
		shiftRegister.writeSRL(led_list, True)
		time.sleep(float(DelayUntiPressed)*(1/speedUp))
		
		shiftRegister.clearAll()
		msg = QtGui.QMessageBox()
		msg.setWindowTitle(u"Τέλος Τραγουδιού!")
		msg.setText(u"Το τραγούδι τελείωσε! Αν θέλετε μπορείτε να επιλέξετε άλλο τραγούδι και να παίξετε ξανά!")
		msg.exec_()
	
		shiftRegister.clearAll()
		
		MainWindow.setEnabled(True)  # Make the window visible/Enabled again
		self.playingSong = False
		return
		

	def exitApp(self):
		shiftRegister.clearAll()  # Clear all the leds before closing
		sys.exit()

        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
	