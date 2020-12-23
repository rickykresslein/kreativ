'''
Documentation, License etc.

@package Kreativ
'''
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import QDate
from datetime import date, timedelta

import pandas as pd

FILENAME = 'creative_hours.csv'

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kreativ')
        self.setLayout(qtw.QVBoxLayout())
        
        self.file_empty = False
        self.df = pd.DataFrame([], columns=['Date', 'Hours'])
        self.today = date.today()
        
        self.build_gui()
        self.read_csv(launch=True)
        
        self.show()
        
    def build_gui(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())
        
        # Create radio button group
        calc_button_group = qtw.QButtonGroup()
        
        # Fields
        kreativ_lbl = qtw.QLabel('Kreativ')
        date_field = qtw.QDateEdit()
        date_field.setDisplayFormat("MM/dd/yyyy")
        date_field.setDate(self.today)
        date_field.setMinimumDate(QDate(1900, 1, 1))
        date_field.setMaximumDate(self.today)
        date_inst = qtw.QLabel('Date to alter')
        hours_field = qtw.QDoubleSpinBox()
        hours_inst = qtw.QLabel('# of creative hours')
        btn_add = qtw.QPushButton('Add', clicked = lambda:self.add_hours(date_field.date().toString('yyyy-MM-dd'), hours_field.value(), 'add'))
        btn_change = qtw.QPushButton('Change', clicked = lambda:self.add_hours(date_field.date().toString('yyyy-MM-dd'), hours_field.value(), 'change'))
        self.notify_lbl = qtw.QLabel('')
        self.notify_lbl.setWordWrap(True)
        rads = [qtw.QRadioButton('Today'), qtw.QRadioButton('Yesterday'), qtw.QRadioButton('Past 30 Days'), qtw.QRadioButton('Past Year'), qtw.QRadioButton('Year:')]
        year_combo = qtw.QComboBox()
        btn_calc = qtw.QPushButton('Calculate', clicked = lambda:self.calc_hours(calc_button_group.checkedId()))
        
        # Add to drop-down
        # TODO Show only years that exist in the file
        year_combo.addItem('2020')
        
        # Add elements to layout
        container.layout().addWidget(kreativ_lbl,0,0,1,2)
        container.layout().addWidget(date_field,1,0,1,1)
        container.layout().addWidget(date_inst,1,1,1,1)
        container.layout().addWidget(hours_field,2,0,1,1)
        container.layout().addWidget(hours_inst,2,1,1,1)
        container.layout().addWidget(btn_add,3,0,1,1)
        container.layout().addWidget(btn_change,3,1,1,1)
        container.layout().addWidget(self.notify_lbl,4,0,1,2)
        for i in range(len(rads)):
            # Add each radio button to container layout
            container.layout().addWidget(rads[i],i+5,0,1,1)
            # Add each radio button to the button group
            calc_button_group.addButton(rads[i],i)
        container.layout().addWidget(year_combo,9,1,1,1)
        container.layout().addWidget(btn_calc,10,0,1,2)
        self.layout().addWidget(container)
        
    def read_csv(self,launch=False):
        self.file_empty = False
        try:
            self.df = pd.read_csv(FILENAME)
            if launch:
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('Hours file found and loaded.')
        except FileNotFoundError:
            self.file_empty = True
            if launch:
                self.notify_lbl.setStyleSheet('color: red')
                self.notify_lbl.setText('File not found. Created file.')
        except ValueError:
            self.file_empty = True
            if launch:
                self.notify_lbl.setStyleSheet('color: red')
                self.notify_lbl.setText('File empty. Add hours.')
            
    def write_csv(self, new_row, method):
        if new_row.get('Date') in self.df['Date'].values:
            if not new_row.get('Hours'):
                self.notify_lbl.setStyleSheet('color: red')
                self.notify_lbl.setText('Hours already exist for that date.')
            elif method == 'add':
                old_hours = self.df._get_value((self.df.Date[self.df.Date == new_row.get('Date')].index[0]), 'Hours')
                self.df.loc[(self.df.Date == new_row.get('Date')),'Hours'] = new_row.get('Hours') + old_hours
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('Hours added to previous total.')
            else:
                self.df.loc[(self.df.Date == new_row.get('Date')),'Hours'] = new_row.get('Hours')
                self.notify_lbl.setStyleSheet('color: green')
                self.notify_lbl.setText('Hours changed to new total.')
        else:
            self.df.loc[len(self.df.index)] = new_row
            self.notify_lbl.setStyleSheet('color: green')
            self.notify_lbl.setText('Hours recorded.')
        self.df.to_csv(FILENAME, index=False)
        
    def add_hours(self, the_date, the_hours, method):
        new_row = {'Date':the_date, 'Hours':the_hours}
        self.write_csv(new_row, method)
        
    def calc_hours(self, sel_rad):
        hours_msg = qtw.QMessageBox()
        hours_msg.setIcon(qtw.QMessageBox.Information)
        warn_msg = qtw.QMessageBox()
        warn_msg.setIcon(qtw.QMessageBox.Warning)
        
        # Read the file again to get any changes
        self.read_csv()
        
        # Make sure the whole file is not empty
        if not self.file_empty:
            # Show Today's hours
            if sel_rad == 0:
                try:
                    total_hours = self.df._get_value((self.df.Date[self.df.Date == self.today.strftime("%Y-%m-%d")].index[0]), 'Hours')
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText(f'{self.formatNumber(total_hours)} creative hours today.')
                except IndexError:
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No hours recorded today.')
            # Show Yesterday's hours
            elif sel_rad == 1:
                try:
                    yesterday = self.today - timedelta(days=1) 
                    total_hours = self.df._get_value((self.df.Date[self.df.Date == yesterday.strftime("%Y-%m-%d")].index[0]), 'Hours')
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText(f'{self.formatNumber(total_hours)} creative hours yesterday.')
                except IndexError:
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No hours recorded yesterday.')
            # Show hours in the last 30 days
            elif sel_rad == 2:
                total_hours = 0
                index_errors = 0
                for i in range(0, 30):
                    day = self.today - timedelta(days=i)
                    try:
                        total_hours += self.df._get_value((self.df.Date[self.df.Date == day.strftime("%Y-%m-%d")].index[0]), 'Hours')
                    except IndexError:
                        index_errors += 1
                if index_errors < 30:
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText(f'{self.formatNumber(total_hours)} creative hours in the past 30 days.')
                else:
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No hours recorded in the last 30 days.')
            # Show hours in the last year
            elif sel_rad == 3:
                total_hours = 0
                index_errors = 0
                for i in range(0, 365):
                    day = self.today - timedelta(days=i)
                    try:
                        total_hours += self.df._get_value((self.df.Date[self.df.Date == day.strftime("%Y-%m-%d")].index[0]), 'Hours')
                    except IndexError:
                        index_errors += 1
                if index_errors < 365:
                    self.notify_lbl.setStyleSheet('color: green')
                    self.notify_lbl.setText(f'{self.formatNumber(total_hours)} creative hours in the past 365 days.')
                else:
                    self.notify_lbl.setStyleSheet('color: red')
                    self.notify_lbl.setText('No hours recorded in the last 365 days.')
            # TODO Show hours in the selected year
            # TODO Listen to podcast part again to know what other times to do.
        # Show a warning if the file is empty.
        else:
            warn_msg.setText("The creative_hours.csv file is empty.")
            warn_msg.setInformativeText("Add some hours to sort the data.")
            warn_msg.setWindowTitle("Creative Hours File Empty")
            warn_msg.exec_()
    
    @staticmethod
    def formatNumber(num):
        if num % 1 == 0:
            return int(num)
        else:
            return num


app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
