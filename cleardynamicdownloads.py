from PyQt6 import QtWidgets, QtCore

class Ui_ClearDynamicDownloads(QtWidgets.QDialog):
    def __init__(self, names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clear Dynamic Downloads")
        self.setMinimumSize(300, 200)

        # Create a vertical layout
        layout = QtWidgets.QVBoxLayout(self)

        # Create a QLabel for the message
        self.message_label = QtWidgets.QLabel(f"Do you really want to delete all <b>{len(names)}</b> dynamically downloaded cosmetics?", self)
        layout.addWidget(self.message_label)  # Add the label to the layout

        # Create a QScrollArea for the names
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Make the scroll area resizeable

        # Create a QWidget to hold the names
        self.names_widget = QtWidgets.QWidget()
        self.names_layout = QtWidgets.QVBoxLayout(self.names_widget)

        # Add names to the layout
        for name in names:
            name_label = QtWidgets.QLabel(name, self.names_widget)
            self.names_layout.addWidget(name_label)

        self.names_widget.setLayout(self.names_layout)
        self.scroll_area.setWidget(self.names_widget)  # Set the names widget in the scroll area
        layout.addWidget(self.scroll_area)  # Add the scroll area to the main layout

        # Create buttons
        self.yes_button = QtWidgets.QPushButton("Yes", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)

        # Connect buttons to their respective methods
        self.yes_button.clicked.connect(self.on_yes)
        self.cancel_button.clicked.connect(self.on_cancel)

        # Add buttons to a horizontal layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def on_yes(self):
        print("Yes pressed. Proceeding to clear dynamic downloads.")
        self.accept()  # Close the dialog with accepted status

    def on_cancel(self):
        self.reject()  # Close the dialog with rejected status
