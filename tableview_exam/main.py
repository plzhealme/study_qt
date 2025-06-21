import os
import qtmodern.styles

from PySide2 import QtWidgets, QtGui, QtCore
from importlib import reload
from ui import table_ui
from model import asset_model

reload(table_ui)
reload(asset_model)



class MainUI(QtWidgets.QWidget, table_ui.Ui_MainWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.asset_model = None
        self.asset_model_proxy = QtCore.QSortFilterProxyModel()
        self.asset_model_proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.asset_model_proxy.setFilterKeyColumn(-1)        
        self.asset_model_delegate = asset_model.AssetItemDelegate()
        self.tableView.setItemDelegate(self.asset_model_delegate)

        self.connected()

    def connected(self):
        self.pushButton.clicked.connect(self.set_model)
        self.searchLineEdit.textChanged.connect(self.filter_items)
        self.asset_model_delegate.button_clicked.connect(self.print_btn_event)
        self.asset_model_delegate.cmb_index_changed.connect(self.print_combo_event)

    def set_model(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        asset_datas = [
            {"name": "AssetA", "id": 1, "version": 3, "thumbnail": f"{current_path}/src/ch.png"},
            {"name": "test_item", "id": 13, "version": 2, "thumbnail": f"{current_path}/src/ch.png"},
            {"name": "some_word", "id": 16, "version": 7, "thumbnail": f"{current_path}/src/ch.png"},
        ]
        self.asset_model = asset_model.AssetModel(row_data=asset_datas)
        self.asset_model_proxy.setSourceModel(self.asset_model)
        self.tableView.setModel(self.asset_model_proxy)
        self.attach_widget()

    @QtCore.Slot(object, str, object)
    def print_combo_event(self, row_data: asset_model.AssetData, version: str, index: QtCore.QModelIndex):
        print(row_data, version, index)

    @QtCore.Slot(object)
    def print_btn_event(self, index: QtCore.QModelIndex):
        row_data: asset_model.AssetData = self.asset_model_proxy.data(index, role=QtCore.Qt.UserRole)
        print(f"Selected asset name is {row_data.name}")
        print(f"Selected asset version is {row_data.version}")

    def filter_items(self):
        filter_text = self.searchLineEdit.text()
        if ' ' in filter_text:
            filter_text = ' '.join(filter_text.split(' '))

        if ',' in filter_text:
                filter_text = '|'.join(filter_text.split(','))

        search = QtCore.QRegExp(filter_text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp)

        self.asset_model_proxy.setFilterRegExp(search)
        self.tableView.setModel(self.asset_model_proxy)
        self.attach_widget()

    def attach_widget(self):
        for row in range(self.asset_model_proxy.rowCount()):            
            combo_index: QtCore.QModelIndex = self.asset_model_proxy.index(row, 4)
            btn_index: QtCore.QModelIndex = self.asset_model_proxy.index(row, 5)

            self.tableView.openPersistentEditor(combo_index)
            self.tableView.openPersistentEditor(btn_index)



def run():
    app = QtWidgets.QApplication()
    qtmodern.styles.dark(app)
    execute_main= MainUI()
    execute_main.show()
    app.exec_()

if __name__ == "__main__":
    run()

