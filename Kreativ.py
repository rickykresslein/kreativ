import os, sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from datetime import date, timedelta, datetime
import base64

import pandas as pd

FILENAME = 'creative_hours.csv'
FILEDIR = os.path.join(os.path.expanduser('~'),'Documents', 'Kreativ')
if not os.path.isdir(FILEDIR):
    os.makedirs(FILEDIR)
FILEPATH = os.path.join(FILEDIR, FILENAME)
image_base64 = b"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"

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kreativ')
        # self.setWindowIcon(qtg.QIcon('Kreativ.ico'))
        # Set base64 icon
        icon = self.iconFromBase64(image_base64)
        self.setWindowIcon(icon)

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

        # Create quit file menu action
        quit_action = file_menu.addAction('Quit', qtw.QApplication.quit, qtg.QKeySequence.Quit)
        
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
    
    @staticmethod
    def iconFromBase64(base64):
        pixmap = qtg.QPixmap()
        pixmap.loadFromData(qtc.QByteArray.fromBase64(base64))
        icon = qtg.QIcon(pixmap)
        return icon

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
