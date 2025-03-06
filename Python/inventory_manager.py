
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

import sys
from os import path
from PyQt5.uic import loadUiType

FROM_CLASS,_=loadUiType(path.join(path.dirname('__file__'),"main.ui"))
import sqlite3


class Main(QMainWindow, FROM_CLASS):

    def __init__(self, parent = None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()


    def Handle_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.next_btn.clicked.connect(self.show_next_tab)
        self.previous_btn.clicked.connect(self.show_previous_tab)
        self.delete_btn.clicked.connect(self.delete_data)
        self.ok_btn.clicked.connect(self.ok_update)

    def GET_DATA(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        command = ''' SELECT * from parts_table '''

        result = cursor.execute(command)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    
    def show_next_tab(self):
        """Show the next tab in the QTabWidget"""
        current_index = self.tabWidget.currentIndex()  
        next_index = current_index + 1 
        
        
        if next_index >= self.tabWidget.count():
            next_index = 0
        
        self.tabWidget.setCurrentIndex(next_index)  

    def show_previous_tab(self):
        """Show the previous tab in the QTabWidget"""
        current_index = self.tabWidget.currentIndex()  
        prev_index = current_index - 1  
        
        
        if prev_index < 0:
            prev_index = self.tabWidget.count() - 1
        
        self.tabWidget.setCurrentIndex(prev_index)

    def delete_data(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        # Get name and age to delete
        reference = self.reference.text()
        part_name = self.part_name.text()

       
        if (reference.strip(), part_name.strip()):  # Check if age is valid
            try:
                # Delete query to remove record based on both name and age
                delete_query = "DELETE FROM parts_table WHERE Reference = ? AND PartName = ?"
                cursor.execute(delete_query, (reference, part_name))
                db.commit()

                if cursor.rowcount > 0:
                    self.show_label.setText("Deleted")
                else:
                    self.show_label.setText("Not Found in Database")

                self.reference.clear()  # Clear name input field after deletion
                self.part_name.clear()   # Clear age input field after deletion
            except sqlite3.DatabaseError as err:
                self.show_label.setText(f"Error: {err}")
        else:
            self.show_label.setText("Please enter both name and a valid age to delete.")

    def ok_update(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()

        id = self.update_txt.text()
        new_reference = self.reference.text()
        new_part_name = self.part_name.text()
        new_min_area = self.min_area.text()
        new_max_area = self.max_area.text()
        new_number_of_holes = self.number_of_holes.text()
        new_min_diameter = self.min_diameter.text()
        new_max_diameter = self.max_diameter.text()
        new_count = self.count.text()

        if id.strip().isdigit() == cursor.ID:
            self.show_label.setText("Ok to Update")
        else:
            self.show_label.setText("Invalid Input Please Enter Item ID")
            try:
                if (new_reference.strip() and new_part_name.strip() and 
                        new_min_area.strip().isdigit() and new_max_area.strip().isdigit() and 
                        new_number_of_holes.strip().isdigit() and new_min_diameter.strip().isdigit()
                        and new_max_diameter.strip().isdigit() and new_count.strip().isdigit()):             
                        
                        update_query = '''UPDATE parts_table 
                                        SET Reference = ? PartName = ?, MinArea = ?, MaxArea = ?, NumberOfHoles = ?, MinDiameter = ?,
                                        MaxDiameter = ?, Count = ? WHERE ID = ?'''
                        
                        cursor.execute(update_query, (new_reference,new_part_name,new_min_area,new_max_area,
                                                    new_number_of_holes,new_min_diameter,new_max_diameter,
                                                    new_count, id))
                        db.commit()
                    
                        if cursor.rowcount > 0:
                            self.show_label.setText("Updated Successfully")
                        else:
                            self.show_label.setText("ID not found")

                    # Clear the input fields after updating
                        self.reference.clear()
                        self.part_name.clear()
                        self.min_area.clear()
                        self.max_area.clear()
                        self.number_of_holes.clear()
                        self.min_diameter.clear()
                        self.max_diameter.clear()
                        self.count.clear()
                        self.id.clear()

            except sqlite3.DatabaseError as error:
                        self.show_label.setText(f"Error: {error}")
            else:
                    self.show_label.setText("Please fill in all fields to update data.") 
            if cursor.rowcount > 0:
                    self.show_label.setText("Updated Successfully")


def main():
    app=QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()