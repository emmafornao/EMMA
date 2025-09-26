import sys
import os
import psutil
import json
import shutil
from pathlib import Path
from datetime import datetime
import logging
import webbrowser

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableView, QVBoxLayout, QMessageBox, QMenu, QWidget, QApplication, QFileDialog
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QEvent, QModelIndex, Qt
# UI Windows
from mainwindow import Ui_MainWindow
from cleardynamicdownloads import Ui_ClearDynamicDownloads
from curseforgeapihandler import API_Handler

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # Set up the UI

        # Logger
        # Create data folder in case it doesn't exist yet
        os.makedirs('data', exist_ok = True)

        # Create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create a FileHandler
        file_handler = logging.FileHandler('data/events.log')
        file_handler.setLevel(logging.DEBUG)  # Set the handler's logging level

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(file_handler)


        # Config
        self.config_file_path = 'data/config.json'
        self.config = self.load_config()

        # keep copies that are updated whenever load_data_from_json() is called
        self.library = {}
        self.favourites = {}

        # API Handler
        self.api_handler = API_Handler()

        # UI
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
        self.installed_model.setHorizontalHeaderLabels(["name", "mod id", "dateUpdated", "dateInstalled", "pathOnDisk", "installedVersion", "installedVersionID", "latestVersion", "latestVersionID"])
        self.favourites_model.setHorizontalHeaderLabels(["name", "mod id", "dateUpdated", "dateInstalled", "pathOnDisk", "installedVersion", "installedVersionID", "latestVersion", "latestVersionID"])


        # Load library.json
        # self.config.get("library_path", "") = r"D:\SteamLibrary\steamapps\common\ARK Survival Ascended\ShooterGame\Binaries\Win64\ShooterGame\ModsUserData\83374\library.json"
        # self.library_path = self.config.get("library_path", "")
        # self.modsuserdata_dir = os.path.dirname(self.config.get("library_path", ""))
        # self.mods_dir = os.path.join(os.path.dirname(os.path.dirname(self.modsuserdata_dir)), "Mods")
        try:
            self.load_data_from_json(self.config.get("library_path", ""), self.installed_model)
        except Exception as e:
            print(f"Config file does not exist or is missing library_path. Please select your ark folder. Error: {e}")


        self.favourites_path = "data/favourites.json"

        # Create favourites.json if it's missing
        if not os.path.exists(self.favourites_path):
            if "favourites" in str(self.favourites_path):  # Check if it's the favourites file
                with open(self.favourites_path, 'w') as file:
                    json.dump({"installedMods": []}, file, indent=4)  # Create an empty structure

        # Load favourites.json
        self.load_data_from_json(self.favourites_path, self.favourites_model)

        """ # Connect the button click signal
        self.pushButton_ToggleFavourite.clicked.connect(self.toggle_favourite) """

        self.pushButton_clearDynamicDownloads.clicked.connect(self.clear_dynamic_downloads)
        self.pushButton_removeMods.clicked.connect(self.uninstall_mods)
        self.pushButton_reinstallMods.clicked.connect(self.reinstall_mods)

        self.action_select_ark_folder.triggered.connect(self.select_ark_folder)
        self.action_settings.triggered.connect(self.settings_menu)
        self.action_about.triggered.connect(self.about_menu)

    def load_config(self):
        try:
            with open(self.config_file_path, 'r', encoding='utf-8-sig') as config_file:
                return json.load(config_file)
        except Exception as e:
            self.logger.error('Failed to load config.json: %s', e)
            try:
                # Create config.json if it's missing
                if not os.path.exists(self.config_file_path):
                    if "config" in str(self.config_file_path):  # Check if it's the favourites file
                        with open(self.config_file_path, 'w') as file:
                            self.config = {
                                "game_path": "",
                                "library_path": "",
                                "mods_path": ""
                            }
                            json.dump(self.config, file, indent=4)  # Create an empty structure
                self.logger.info('config.json has been created.')
            except Exception as e:
                self.logger.error('Failed to create config.json: %s', e)
    
    def save_config(self):
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as config_file:
                json.dump(self.config, config_file, indent=4)
                # self.logger.info('Config saved successfully.')
        except Exception as e:
            self.logger.error('Failed to save config.json: %s', e)    

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
        # menu.addAction("Uninstall").setData("uninstall")
        # menu.addAction("Reinstall").setData("reinstall")
        menu.addAction("Open Website").setData("open_website")

        action = menu.exec(event.globalPos())
        self.handleFavouritesMenuAction(action, row)

    def handleInstalledMenuAction(self, action, row):
        if action:
            action_data = action.data()
            if action_data == "select_all":
                print("Select All action triggered")
                # Implement Select All functionality
                self.tableView_installed.selectAll()
            elif action_data == "add_to_favourites":
                print(f"Add to Favourites action triggered for row {row}")
                # Implement Add to Favourites functionality using row
                # self.add_to_favourites_from_row(row)
                self.add_to_favourites_from_row()
            elif action_data == "uninstall":
                print(f"Uninstall action triggered for row {row}")
                # Implement Uninstall functionality using row

                # Determine the row index based on the context
                if row is None:  # If no row is provided, use the current index
                    selected_index = self.tableView_installed.currentIndex()
                    if not selected_index.isValid():
                        QMessageBox.warning(self, "Warning", "No mod selected.")
                        return
                    row = selected_index.row()  # Get the row from the current index

                mod_id = int(self.installed_model.item(row, 1).text())
                mod_ids = set()
                mod_ids.add(mod_id)         
                self.uninstall_mods(mod_ids)
            elif action_data == "reinstall":
                print(f"Reinstall action triggered for row {row}")
                # Implement Reinstall functionality using row

                # Determine the row index based on the context
                if row is None:  # If no row is provided, use the current index
                    selected_index = self.tableView_installed.currentIndex()
                    if not selected_index.isValid():
                        QMessageBox.warning(self, "Warning", "No mod selected.")
                        return
                    row = selected_index.row()  # Get the row from the current index

                mod_id = int(self.installed_model.item(row, 1).text())
                mod_ids = set()
                mod_ids.add(mod_id)         
                self.reinstall_mods(mod_ids)
            elif action_data == "open_website":
                print(f"Open Website action triggered for row {row}")
                # Implement Open Website functionality using row
                self.open_mod_website(row, "installed")

    def handleFavouritesMenuAction(self, action, row):
        if action:
            action_data = action.data()
            if action_data == "select_all":
                print("Select All action triggered")
                # Implement Select All functionality
                self.tableView_favourites.selectAll()
            elif action_data == "remove_from_favourites":
                print(f"Remove from Favourites action triggered for row {row}")
                self.remove_from_favourites_from_row(row)
                # Implement Remove from Favourites functionality using row
            # elif action_data == "uninstall":
            #     print(f"Uninstall action triggered for row {row}")
            #     # Implement Uninstall functionality using row
            # elif action_data == "reinstall":
            #     print(f"Reinstall action triggered for row {row}")
            #     # Implement Reinstall functionality using row
            elif action_data == "open_website":
                print(f"Open Website action triggered for row {row}")
                # Implement Open Website functionality using row
                self.open_mod_website(row, "favourites")

    def open_mod_website(self, row, tableViewName):
        # modId = self.favourites_model.item(row, 1).text() # Assuming mod id is in second column

        weblink = ""

        if tableViewName == "installed":
            modId = int(self.installed_model.item(row, 1).text())

            for mod in self.library:
                if mod.get("details", {}).get("iD", "") == modId:
                    weblink = mod.get("details", {}).get("links", {}).get("websiteUrl", "")
                    break

        elif tableViewName == "favourites":
            modId = int(self.favourites_model.item(row, 1).text())

            for mod in self.library: # while we need to check the favourites_model for the selected mod, the URL is currently not saved in favourites and therefore we need to search library instead
                if mod.get("details", {}).get("iD", "") == modId:
                    weblink = mod.get("details", {}).get("links", {}).get("websiteUrl", "")
                    break
        
        webbrowser.open(weblink)

    def load_data_from_json(self, file_path, model):
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                data = json.load(file)  # Load the JSON data

            # Access the list of installed mods
            installed_mods = data.get("installedMods", [])

            if "library.json" in file_path:
                    self.library = installed_mods
            elif "favourites.json" in file_path:
                self.favourites = installed_mods

            for mod in installed_mods:
                # print(mod)

                name = mod.get("details", {}).get("name", "")
                modId = mod.get("details", {}).get("iD", "")
                dateUpdated = mod.get("dateUpdated", "")
                dateInstalled = mod.get("dateInstalled", "")
                pathOnDisk = mod.get("pathOnDisk", "")
                installedVersion = mod.get("installedFile", {}).get("filename", "")
                installedVersionID = mod.get("installedFile", {}).get("iD", "")
                latestVersion = mod.get("latestUpdatedFile", {}).get("filename", "")
                latestVersionID = mod.get("latestUpdatedFile", {}).get("iD", "")

                # Create a row with the extracted data
                row = [QStandardItem(name), QStandardItem(str(modId)), QStandardItem(dateUpdated), QStandardItem(dateInstalled), QStandardItem(pathOnDisk), QStandardItem(installedVersion), QStandardItem(str(installedVersionID)), QStandardItem(latestVersion), QStandardItem(str(latestVersionID))]
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
        # reload self.favourites from file?

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
            modId = self.favourites_model.item(row, 1).text()
            date_updated = self.favourites_model.item(row, 2).text()
            date_installed = self.favourites_model.item(row, 3).text()
            path_on_disk = self.favourites_model.item(row, 4).text()
            installed_version = self.favourites_model.item(row, 5).text()
            installed_version_id = self.favourites_model.item(row, 6).text()
            latest_version = self.favourites_model.item(row, 7).text()
            latest_version_id = self.favourites_model.item(row, 8).text()

            # Append each mod's data as a dictionary to the installedMods list
            favourites_data["installedMods"].append({
                "dateUpdated": date_updated,
                "dateInstalled": date_installed,
                "pathOnDisk": path_on_disk,
                "details": {
                    "iD": modId,
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
        with open(self.favourites_path, 'w') as file:
            json.dump(favourites_data, file, indent=4)

    def uninstall_mods(self, mod_ids_to_remove):
        # Check if ArkAscended.exe is running
        if self.is_process_running("ArkAscended.exe"):
            print("ArkAscended.exe is running. Please close it before making changes.")
        else:
            try:
                with open(self.config.get("library_path", ""), 'r', encoding='utf-8-sig') as file: # loading from file instead of self.library just in case something changed. could also refresh self.library right before instead
                    data = json.load(file)  # Load the JSON data

                # Access the list of installed mods
                installed_mods = data.get("installedMods", [])
                print(mod_ids_to_remove)
                mods_to_remove = {}

                for mod in installed_mods:
                    if mod.get("details", {}).get("iD", "") in mod_ids_to_remove:
                        name = mod.get("details", {}).get("name", "")
                        path = mod.get("pathOnDisk", "")
                        print(path)
                        mods_to_remove[path] = name
                
                if not mods_to_remove:
                    print("mod not found - mods_to_remove is empty")

                dialog = Ui_ClearDynamicDownloads(mods_to_remove.values(), self)
                if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    # Code to execute when Yes is pressed
                    # print("Dialog accepted.")

                    # Remove matching entries from installed_mods
                    updated_installed_mods = [
                        mod for mod in installed_mods if mod.get("details", {}).get("iD", "") not in mod_ids_to_remove
                    ]
                    
                    
                    # Update the data dictionary
                    data["installedMods"] = updated_installed_mods


                    for folder in mods_to_remove.keys():

                        # Create the full path to the folder so it can be deleted
                        try:
                            folder_path = self.config.get("mods_path", "") + folder
                        except Exception as e:
                            print(f"Mod path missing in config file. Did you select your Ark Folder yet? Error: {e}")
                        

                        # Check if the directory exists before attempting to delete
                        if os.path.exists(folder_path):
                            try:
                                shutil.rmtree(folder_path)
                                print(f"'{folder_path}' has been deleted successfully.")
                            except Exception as e:
                                print(f"An error occurred: {e}")
                                self.logger.error({e})
                        else:
                            print(f"'{folder_path}' does not exist.")
                            self.logger.warning('Mod folder %s does not exist and can not be deleted.', folder)

                        # Write using logger
                        self.log_event("UNINSTALL", mods_to_remove[folder], f'Path: {folder}')
                    

                    # Write the updated data back to the JSON file - done after the log and file delete so we don't mess up the library.json in case something went wrong
                    with open(self.config.get("library_path", ""), 'w', encoding='utf-8-sig') as file:
                        json.dump(data, file)



            except Exception as e:
                print(f"Error loading JSON data: {e}")

    def reinstall_mods(self, mod_ids):
        
        # self.uninstall_mods(mod_ids)

        download_links = {}
        for mod in mod_ids:
            download_links[mod] = self.api_handler.get_download_link(mod)
            print("mod ", mod, " has main file id: ", download_links[mod])
            self.api_handler.download_mod(mod, download_links[mod])



    def is_process_running(self, process_name):
        # Iterate over all running processes
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def log_event(self, eventType, eventName, addInfo):
        """ # Open the log file in append mode
        with open(self.log_file_path, 'a', encoding='utf-8-sig') as log_file:

                # Get the current time
                current_time = datetime.now().isoformat()
                
                # Write to the log file
                log_file.write(f"{current_time}    {eventType}    {eventName}    {addInfo}\n") """
        self.logger.info('%s - %s - %s', eventType, eventName, addInfo)

    def clear_dynamic_downloads(self):
        # make sure game is closed
        # open library.json (library_path) with 'w' rights
        # find all mods that have "dynamicContent": true
        # add the pathOnDisk of those mods to an array
        # list all mods in a popup by name and have user confirm to remove them
        # delete their entry in library.json
        # close library.json, go one folder up from it, go to Mods folder and then delete all folders that have the names in the new pathOnDisk array

        # Check if ArkAscended.exe is running
        if self.is_process_running("ArkAscended.exe"):
            print("ArkAscended.exe is running. Please close it before making changes.")
        else:
            try:
                with open(self.config.get("library_path", ""), 'r', encoding='utf-8-sig') as file: # loading from file instead of self.library just in case something changed. could also refresh self.library right before instead
                    data = json.load(file)  # Load the JSON data

                # Access the list of installed mods
                installed_mods = data.get("installedMods", [])

                dynamicmod_modId = set()
                dynamic_mods = {}

                for mod in installed_mods:
                
                    if mod.get("dynamicContent") == True:
                        # print("found dynamically downloaded mod: ", mod.get("details", {}).get("name", ""), ", pathOnDisk: ", mod.get("pathOnDisk", ""))
                        dynamicmod_modId.add(mod.get("details", {}).get("iD", ""))
                        name = mod.get("details", {}).get("name", "")
                        path = mod.get("pathOnDisk", "")
                        dynamic_mods[path] = name
                        # print(mod)
                

                dialog = Ui_ClearDynamicDownloads(dynamic_mods.values(), self)
                if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    # Code to execute when Yes is pressed
                    # print("Dialog accepted.")

                    # Remove matching entries from installed_mods
                    updated_installed_mods = [
                        mod for mod in installed_mods if mod.get("details", {}).get("iD", "") not in dynamicmod_modId
                    ]
                    
                    """ print("mods remaining: ")
                    for mod in updated_installed_mods:
                        print(mod.get("details", {}).get("name", "")) """
                    
                    # Update the data dictionary
                    data["installedMods"] = updated_installed_mods

                    # Open the log file in append mode
                    # with open(self.log_file_path, 'a', encoding='utf-8-sig') as log_file:

                    for folder in dynamic_mods.keys():

                        # Create the full path to the folder so it can be deleted
                        # folder_path = Path(str(self.mods_dir).replace('\\', '/')) / folder
                        try:
                            folder_path = self.config.get("mods_path", "") / folder
                        except Exception as e:
                            print(f"Mod path missing in config file. Did you select your Ark Folder yet? Error: {e}")
                        
                        # Delete the folder
                        # shutil.rmtree(folder_path)

                        # Check if the directory exists before attempting to delete
                        if os.path.exists(folder_path):
                            try:
                                shutil.rmtree(folder_path)
                                print(f"'{folder_path}' has been deleted successfully.")
                            except Exception as e:
                                print(f"An error occurred: {e}")
                                self.logger.error({e})
                        else:
                            print(f"'{folder_path}' does not exist.")
                            self.logger.warning('Mod folder %s does not exist and can not be deleted.', folder)

                        
                        """ # Get the current time
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Write to the log file
                        log_file.write(f"Deleted dynamically downloaded cosmetic: {dynamic_mods[folder]} at {current_time}. Path: {folder}\n") """

                        # Write using logger
                        self.log_event("CLEARDYNAMIC", dynamic_mods[folder], f'Path: {folder}')
                    

                    # Write the updated data back to the JSON file - done after the log and file delete so we don't mess up the library.json in case something went wrong
                    with open(self.config.get("library_path", ""), 'w', encoding='utf-8-sig') as file:
                        json.dump(data, file)
                
                                                                

            except Exception as e:
                print(f"Error loading JSON data: {e}")

    def select_ark_folder(self):
        # self.config.get("library_path", "") 
        # self.config.set("library_path")
        folder = QFileDialog.getExistingDirectory(self,("Open \"ARK Survival Ascended\" Folder"))
        # print(folder)
        # print(folder + "/ShooterGame/Binaries/Win64/ShooterGame/ModsUserData/83374/library.json")
        self.config["game_path"] = folder
        self.config["library_path"] = folder +  "/ShooterGame/Binaries/Win64/ShooterGame/ModsUserData/83374/library.json"
        self.config["mods_path"] = folder + "/ShooterGame/Binaries/Win64/ShooterGame/Mods/"
        # print(self.config.get("library_path", ""))
        self.save_config()
        self.load_data_from_json(self.config.get("library_path", ""), self.installed_model)
    
    def settings_menu(self):
        # make a settings menu
        return None
    
    def about_menu(self):
        # make an about menu

        text = "<center>" \
            "<b>E</b>mma's <b>M</b>od <b>M</b>anager for <b>A</b>rk: Survival Ascended" \
            "&#8291;" \
            "<p>Version 0.0.1<br/>" \
            "<a href='https://github.com/emmafornao/EMMA'>https://github.com/emmafornao/EMMA</a></p>" \
            "</center>"

        msg_box = QMessageBox()
        msg_box.setWindowTitle("About EMMA")
        msg_box.setTextFormat(Qt.TextFormat.RichText)  # Set text format to RichText
        msg_box.setText(text)  # Set the text
        msg_box.exec()  # Show the message box


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create the application instance
    window = MainWindow()  # Create an instance of your main window
    window.show()  # Show the main window
    sys.exit(app.exec())  # Start the application event loop
