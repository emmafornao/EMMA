import sys
import os
import json
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableView, QVBoxLayout, QMessageBox, QMenu, QWidget, QApplication
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QEvent, QModelIndex
from mainwindow import Ui_MainWindow  # Import the generated UI class

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # Set up the UI

        # Create models for the QTableViews
        self.installed_model = QStandardItemModel()
        self.favourites_model = QStandardItemModel()

        # Set models to the QTableViews
        self.tableView_installed.setModel(self.installed_model)
        self.tableView_favourites.setModel(self.favourites_model)

        # Enable sorting
        self.tableView_installed.setSortingEnabled(True)
        self.tableView_favourites.setSortingEnabled(True)

        # Set headers for the tables
        self.installed_model.setHorizontalHeaderLabels(["name", "dateUpdated", "dateInstalled", "pathOnDisk", "installedVersion", "installedVersionID", "latestVersion", "latestVersionID"])
        self.favourites_model.setHorizontalHeaderLabels(["name", "dateUpdated", "dateInstalled", "pathOnDisk", "installedVersion", "installedVersionID", "latestVersion", "latestVersionID"])

        # Load library.json
        self.load_data_from_json(r"D:\SteamLibrary\steamapps\common\ARK Survival Ascended\ShooterGame\Binaries\Win64\ShooterGame\ModsUserData\83374\library.json", self.installed_model)

        # Create favourites.json if it's missing
        if not os.path.exists("favourites.json"):
            if "favourites" in "favourites.json":  # Check if it's the favourites file
                with open("favourites.json", 'w') as file:
                    json.dump({"installedMods": []}, file, indent=4)  # Create an empty structure

        # Load favourites.json
        self.load_data_from_json("favourites.json", self.favourites_model)

        """ # Connect the button click signal
        self.pushButton_ToggleFavourite.clicked.connect(self.toggle_favourite) """

    def eventFilterOLD(self, obj, event):
        if event.type() == QEvent.Type.ContextMenu and obj is self.tableView_installed:
            menu = QMenu()
            menu.addAction("Add to Favourites")

            if menu.exec(event.globalPos()):
                item = obj.rowAt(event.pos().y())
                print(item)

            return True
        return super().eventFilter(obj, event)
    
    def eventFilterROWAT(self, obj, event):
        if event.type() == QEvent.Type.ContextMenu and obj is self.tableView_installed:
            menu = QMenu()
            menu.addAction("Add to Favourites")

            action = menu.exec(event.globalPos())
            
            if action:  # Check if an action was triggered
                # Get the y-coordinate from the event position
                y_pos = event.pos().y()
                # Adjust for the header height
                header_height = obj.horizontalHeader().height()
                adjusted_y_pos = y_pos - header_height
                
                row = obj.rowAt(adjusted_y_pos)  # Get the row index

                if row != -1:  # Ensure the row is valid
                    item = obj.model().index(row, 0)  # Get the model index for the first column
                    print(item.data())  # Print the data of the item

            return True
        return super().eventFilter(obj, event)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ContextMenu:
            # Get the y-coordinate from the event position
            y_pos = event.pos().y()
            # Adjust for the header height
            header_height = obj.horizontalHeader().height()
            adjusted_y_pos = y_pos - header_height
            
            row = obj.rowAt(adjusted_y_pos)  # Get the row index

            if row != -1:  # Ensure the row is valid
                if obj is self.tableView_installed:
                    self.showInstalledContextMenu(event, row)
                    return True
                elif obj is self.tableView_favourites:
                    self.showFavouritesContextMenu(event, row)
                    return True
        return super().eventFilter(obj, event)

    def showInstalledContextMenu(self, event, row):
        menu = QMenu()
        menu.addAction("Select All").setData("select_all")
        menu.addAction("Add to Favourites").setData("add_to_favourites")
        menu.addAction("Uninstall").setData("uninstall")
        menu.addAction("Reinstall").setData("reinstall")
        menu.addAction("Open Website").setData("open_website")

        action = menu.exec(event.globalPos())
        self.handleInstalledMenuAction(action, row)

    def showFavouritesContextMenu(self, event, row):
        menu = QMenu()
        menu.addAction("Select All").setData("select_all")
        menu.addAction("Remove from Favourites").setData("remove_from_favourites")
        menu.addAction("Uninstall").setData("uninstall")
        menu.addAction("Reinstall").setData("reinstall")
        menu.addAction("Open Website").setData("open_website")

        action = menu.exec(event.globalPos())
        self.handleFavouritesMenuAction(action, row)

    def handleInstalledMenuAction(self, action, row):
        if action:
            action_data = action.data()
            if action_data == "select_all":
                print("Select All action triggered")
                # Implement Select All functionality
            elif action_data == "add_to_favourites":
                print(f"Add to Favourites action triggered for row {row}")
                # Implement Add to Favourites functionality using row
                self.add_to_favourites_from_row(row)
            elif action_data == "uninstall":
                print(f"Uninstall action triggered for row {row}")
                # Implement Uninstall functionality using row
            elif action_data == "reinstall":
                print(f"Reinstall action triggered for row {row}")
                # Implement Reinstall functionality using row
            elif action_data == "open_website":
                print(f"Open Website action triggered for row {row}")
                # Implement Open Website functionality using row

    def handleFavouritesMenuAction(self, action, row):
        if action:
            action_data = action.data()
            if action_data == "select_all":
                print("Select All action triggered")
                # Implement Select All functionality
            elif action_data == "remove_from_favourites":
                print(f"Remove from Favourites action triggered for row {row}")
                self.remove_from_favourites_from_row(row)
                # Implement Remove from Favourites functionality using row
            elif action_data == "uninstall":
                print(f"Uninstall action triggered for row {row}")
                # Implement Uninstall functionality using row
            elif action_data == "reinstall":
                print(f"Reinstall action triggered for row {row}")
                # Implement Reinstall functionality using row
            elif action_data == "open_website":
                print(f"Open Website action triggered for row {row}")
                # Implement Open Website functionality using row

            


    def load_data_from_json(self, file_path, model):
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                data = json.load(file)  # Load the JSON data

            # Access the list of installed mods
            installed_mods = data.get("installedMods", [])

            for mod in installed_mods:
                # print(mod)

                name = mod.get("details", {}).get("name", "")
                dateUpdated = mod.get("dateUpdated", "")
                dateInstalled = mod.get("dateInstalled", "")
                pathOnDisk = mod.get("pathOnDisk", "")
                installedVersion = mod.get("installedFile", {}).get("filename", "")
                installedVersionID = mod.get("installedFile", {}).get("iD", "")
                latestVersion = mod.get("latestUpdatedFile", {}).get("filename", "")
                latestVersionID = mod.get("latestUpdatedFile", {}).get("iD", "")

                # Create a row with the extracted data
                row = [QStandardItem(name), QStandardItem(dateUpdated), QStandardItem(dateInstalled), QStandardItem(pathOnDisk), QStandardItem(installedVersion), QStandardItem(str(installedVersionID)), QStandardItem(latestVersion), QStandardItem(str(latestVersionID))]
                model.appendRow(row)  # Add the row to the model

        except Exception as e:
            print(f"Error loading JSON data: {e}")

def add_to_favourites_from_row(self, row=None):
    # Determine the row index based on the context
    if row is None:  # If no row is provided, use the current index
        selected_index = self.tableView_installed.currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Warning", "No mod selected.")
            return
        row = selected_index.row()  # Get the row from the current index

    # Collect all values from the selected row into a list
    row_data = []
    for column in range(self.installed_model.columnCount()):
        item = self.installed_model.item(row, column)
        row_data.append(item.text() if item else "")  # Append the text or an empty string if the item is None

    # Pass the entire row_data list to add_to_favourites
    self.add_to_favourites(row_data)

def add_to_favourites(self, row_data):
    # Create a new row for the favourites model
    row = [QStandardItem(data) for data in row_data]  # Create QStandardItem for each data point
    self.favourites_model.appendRow(row)  # Add the row to the model

    # Save to favourites.json
    self.save_favourites()


    def remove_from_favourites_from_row(self, row):
        name = self.favourites_model.item(row, 0).text()  # Assuming name is in the first column
        for fav_row in range(self.favourites_model.rowCount()):
            if self.favourites_model.item(fav_row, 0).text() == name:
                self.favourites_model.removeRow(fav_row)  # Remove the row from the model
                self.save_favourites()  # Save changes to favourites.json
                return

    def save_favourites(self):
        favourites_data = {"installedMods": []}  # Create a dictionary to hold the installedMods key

        for row in range(self.favourites_model.rowCount()):
            name = self.favourites_model.item(row, 0).text()
            date_updated = self.favourites_model.item(row, 1).text()
            date_installed = self.favourites_model.item(row, 2).text()
            path_on_disk = self.favourites_model.item(row, 3).text()
            installed_version = self.favourites_model.item(row, 4).text()
            installed_version_id = self.favourites_model.item(row, 5).text()
            latest_version = self.favourites_model.item(row, 6).text()
            latest_version_id = self.favourites_model.item(row, 7).text()

            # Append each mod's data as a dictionary to the installedMods list
            favourites_data["installedMods"].append({
                "dateUpdated": date_updated,
                "dateInstalled": date_installed,
                "pathOnDisk": path_on_disk,
                "details": {
                    "name": name,
                },
                "installedFile": {
                    "filename": installed_version,
                    "iD": installed_version_id,
                    
                },
                "latestUpdatedFile": {
                    "filename": latest_version,
                    "iD": latest_version_id
                }
            })

        # Write the structured data to favourites.json
        with open("favourites.json", 'w') as file:
            json.dump(favourites_data, file, indent=4)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create the application instance
    window = MainWindow()  # Create an instance of your main window
    window.show()  # Show the main window
    sys.exit(app.exec())  # Start the application event loop
