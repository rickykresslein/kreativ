'''
Documentation, License etc.

@package Kreativ
'''
import os, sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from datetime import date, timedelta, datetime

import pandas as pd
import base64

FILENAME = 'creative_hours.csv'
FILEDIR = os.path.join(os.path.expanduser('~'),'Documents', 'Kreativ')
if not os.path.isdir(FILEDIR):
    os.makedirs(FILEDIR)
FILEPATH = os.path.join(FILEDIR, FILENAME)

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kreativ')
        # icon2 = qtg.QIcon()
        self.setWindowIcon(qtg.QIcon(os.path.join(os.path.expanduser('~'),'projects/Kreativ/images/icon.ico')))
        # self.setWindowIcon(icon2)
        self.main_layout = qtw.QWidget()
        self.setCentralWidget(self.main_layout)
        self.main_layout.setLayout(qtw.QVBoxLayout())
        
        self.file_empty = False
        self.df = pd.DataFrame([], columns=['Date', 'Hours'])
        self.today = date.today()
        
        self.build_gui()        
        self.read_csv(launch=True)
        
        self.show()
        
    def build_gui(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        
        # Create Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # Create Reload File menu button
        reload_action = qtw.QAction(self)
        reload_action.setText('Reload File')
        reload_action.setShortcut('Ctrl+R')
        reload_action.setStatusTip('Reload Hours CSV')
        reload_action.triggered.connect(lambda:self.read_csv(reloaded=True))
        file_menu.addAction(reload_action)

        # Create backup File menu action
        backup_action = file_menu.addAction('Create Backup', self.backup_file)
        backup_action.setShortcut('Ctrl+B')
        backup_action.setStatusTip('Create a backup of creative_hours.csv')
        
        # Create radio button group
        calc_button_group = qtw.QButtonGroup()
        
        # Fields
        date_field = qtw.QDateEdit()
        date_field.setDisplayFormat("MM/dd/yyyy")
        date_field.setDate(self.today)
        date_field.setMinimumDate(datetime(1900, 1, 1))
        date_field.setMaximumDate(self.today)
        date_field.setCalendarPopup(True)
        date_inst = qtw.QLabel('Date to alter')
        hours_field = qtw.QDoubleSpinBox()
        hours_field.setSingleStep(0.25)
        hours_inst = qtw.QLabel('# of creative hours')
        btn_submit = qtw.QPushButton('Submit', clicked = lambda:self.add_hours(date_field.date().toString('yyyy-MM-dd'), hours_field.value()))
        self.notify_lbl = qtw.QLabel('')
        self.notify_lbl.setWordWrap(True)
        self.notify_lbl.setFixedHeight(50)
        self.notify_lbl.setMaximumWidth(300)
        rads = [
            qtw.QRadioButton('Today'),
            qtw.QRadioButton('Yesterday'),
            qtw.QRadioButton('Past 30 Days'),
            qtw.QRadioButton('Past 90 Days'),
            qtw.QRadioButton('Past 180 Days'),
            qtw.QRadioButton('Past Year'),
            qtw.QRadioButton('Year:'),
        ]
        self.year_combo = qtw.QComboBox()
        btn_calc = qtw.QPushButton('Calculate', clicked = lambda:self.calc_hours(calc_button_group.checkedId()))
        
        # Add elements to layout
        container.layout().addWidget(date_field,0,0,1,1)
        container.layout().addWidget(date_inst,0,1,1,1)
        container.layout().addWidget(hours_field,1,0,1,1)
        container.layout().addWidget(hours_inst,1,1,1,1)
        container.layout().addWidget(btn_submit,2,0,1,2)
        container.layout().addWidget(self.notify_lbl,3,0,1,2)
        for i in range(len(rads)):
            # Add each radio button to container layout
            container.layout().addWidget(rads[i],i+4,0,1,1)
            # Add each radio button to the button group
            calc_button_group.addButton(rads[i],i)
        container.layout().addWidget(self.year_combo,10,1,1,1)
        container.layout().addWidget(btn_calc,11,0,1,2)
        self.main_layout.layout().addWidget(container)
        
    def read_csv(self,launch=False,reloaded=False):
        self.file_empty = False
        try:
            self.df = pd.read_csv(FILEPATH)
            if launch:
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('Hours file found and loaded.')
            elif reloaded:
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('Reloaded hours file.')
            # Add years to combo box
            self.find_listed_years()
        except FileNotFoundError:
            self.file_empty = True
            if launch:
                self.notify_lbl.setStyleSheet('color: red')
                self.notify_lbl.setText('File not found. File will be created when you add some hours.')
        except ValueError:
            self.file_empty = True
            if launch:
                self.notify_lbl.setStyleSheet('color: red')
                self.notify_lbl.setText('File empty. Add hours.')
            
    def write_csv(self, new_row):
        if new_row.get('Date') in self.df['Date'].values:
            old_hours = self.df._get_value((self.df.Date[self.df.Date == new_row.get('Date')].index[0]), 'Hours')
            warn_msg = qtw.QMessageBox()
            warn_msg.setIcon(qtw.QMessageBox.Warning)
            warn_msg.setText(f"That date already contains {old_hours} creative hours.")
            warn_msg.setInformativeText("What would you like to do?")
            warn_msg.setWindowTitle("Date Already Populated")
            warn_msg.addButton(qtw.QPushButton('Cancel'), qtw.QMessageBox.YesRole)
            warn_msg.addButton(qtw.QPushButton('Add'), qtw.QMessageBox.RejectRole)
            warn_msg.addButton(qtw.QPushButton('Change'), qtw.QMessageBox.NoRole)
            msg_choice = warn_msg.exec_()
            if msg_choice == 1:
                if not new_row.get('Hours'):
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No need to add 0 hours.')
                    return
                else:
                    self.df.loc[(self.df.Date == new_row.get('Date')),'Hours'] = new_row.get('Hours') + old_hours
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText('Hours added to previous total.')
            elif msg_choice == 2:
                self.df.loc[(self.df.Date == new_row.get('Date')),'Hours'] = new_row.get('Hours')
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('Hours changed to new total.')
            else:
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('No change applied.')
                return
        else:
            self.df.loc[len(self.df.index)] = new_row
            self.notify_lbl.setStyleSheet('color: green')
            self.notify_lbl.setText('Hours recorded.')
        
        # Write the file
        self.df = self.df.sort_values(by='Date', ascending=True)
        self.df.to_csv(FILEPATH, index=False)
        
    def add_hours(self, the_date, the_hours):
        new_row = {'Date':the_date, 'Hours':the_hours}
        self.write_csv(new_row)
        # Read the file again to get any changes
        self.read_csv()
        
    def calc_hours(self, sel_rad):
        hours_msg = qtw.QMessageBox()
        hours_msg.setIcon(qtw.QMessageBox.Information)
        
        # Make sure the whole file is not empty
        if not self.file_empty:
            # Show Today's hours
            if sel_rad == 0:
                try:
                    total_hours = self.df._get_value((self.df.Date[self.df.Date == self.today.strftime("%Y-%m-%d")].index[0]), 'Hours')
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText(f'{self.format_number(total_hours)} creative hours today.')
                except IndexError:
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No hours recorded today.')
            # Show Yesterday's hours
            elif sel_rad == 1:
                try:
                    yesterday = self.today - timedelta(days=1) 
                    total_hours = self.df._get_value((self.df.Date[self.df.Date == yesterday.strftime("%Y-%m-%d")].index[0]), 'Hours')
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText(f'{self.format_number(total_hours)} creative hours yesterday.')
                except IndexError:
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No hours recorded yesterday.')
            # Show hours in the last 30 days
            elif sel_rad == 2:
                self.scan_days(30)
            # Show hours in the last year
            elif sel_rad == 3:
                self.scan_days(90)
            elif sel_rad == 4:
                self.scan_days(180)
            elif sel_rad == 5:
                self.scan_days(365)
            # Show hours in the selected year
            elif sel_rad == 6:
                sel_year = str(self.year_combo.currentText())
                whole_year = self.df[self.df['Date'].str.contains(sel_year)]
                total_hours = sum(whole_year.Hours.values)
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText(f'{self.format_number(total_hours)} creative hours in {sel_year}.')
        # Show a warning if the file is empty.
        else:
            warn_msg = qtw.QMessageBox()
            warn_msg.setIcon(qtw.QMessageBox.Warning)
            warn_msg.setText("The creative_hours.csv file is empty.")
            warn_msg.setInformativeText("Add some hours to sort the data.")
            warn_msg.setWindowTitle("Creative Hours File Empty")
            warn_msg.exec_()
            
    def scan_days(self, num_days):
        total_hours = 0
        index_errors = 0
        for i in range(0, num_days):
            day = self.today - timedelta(days=i)
            try:
                total_hours += self.df._get_value((self.df.Date[self.df.Date == day.strftime("%Y-%m-%d")].index[0]), 'Hours')
            except IndexError:
                index_errors += 1
        if index_errors < num_days:
            self.notify_lbl.setStyleSheet('color: green')
            self.notify_lbl.setText(f'{self.format_number(total_hours)} creative hours in the past {num_days} days.')
        else:
            self.notify_lbl.setStyleSheet('color: red')
            self.notify_lbl.setText(f'No hours recorded in the last {num_days} days.')
    
    def find_listed_years(self):
        all_values = self.df.Date.values
        all_years = []
        for i in range(0, len(all_values)):
            all_years.append(all_values[i][0:4])
        unq_years = list(set(all_years))
        unq_years.sort(reverse=True)
        self.year_combo.clear()
        self.year_combo.addItems(unq_years)

    def backup_file(self):
        backup_filename = os.path.join(FILEDIR, 'creative_hours.bak')
        self.notify_lbl.setStyleSheet('color: green')
        self.notify_lbl.setText(f'Backup created: ~/Documents/Kreativ/creative_hours.bak')
        self.df = self.df.sort_values(by='Date', ascending=True)
        self.df.to_csv(backup_filename, index=False)
    
    @staticmethod
    def format_number(num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
