from PySide2 import QtCore, QtGui, QtWidgets

class AssetData(object):
    def __init__(self, data_dict):
        self.name = data_dict['name']
        self.id = data_dict['id']
        self.version = data_dict['version']
        self.thumbnail = data_dict['thumbnail']
        self.item = data_dict

class AssetModel(QtCore.QAbstractTableModel):
    HORIZONTAL_HEADERS = ['image', 'name', 'id', 'version', 'combo', 'btn']

    def __init__(self, row_data=None, parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.entri_data = []
        for data_dict in row_data:
            item = AssetData(data_dict)
            self.entri_data.append(item)

    def rowCount(self, parent):
        return len(self.entri_data)

    def columnCount(self, parent):
        return len(self.HORIZONTAL_HEADERS)

    def headerData(self, row, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return self.HORIZONTAL_HEADERS[row]
        if orientation == QtCore.Qt.Vertical:
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QAbstractTableModel.headerData(self, row, orientation, role)

    def data(self, index: QtCore.QModelIndex, role):
        row: int = index.row()
        column: int = index.column()
        item: AssetData = self.entri_data[row]

        if role == QtCore.Qt.DisplayRole:
            if column == 1:                
                return item.name
            elif column == 2:                
                return item.id
            elif column == 3:
                return item.version
        elif role == QtCore.Qt.DecorationRole:
            if column == 0:
                thumb = QtGui.QPixmap(item.thumbnail).scaled(QtCore.QSize(100, 100), QtCore.Qt.KeepAspectRatio)
                return thumb
        elif role == QtCore.Qt.UserRole:
            return item
        return None

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    

class AssetItemDelegate(QtWidgets.QItemDelegate):
    button_clicked = QtCore.Signal(object)
    cmb_index_changed = QtCore.Signal(object, str, object)

    def __init__(self, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        column = index.column()
        row_data: AssetData = index.data(QtCore.Qt.UserRole)

        editor = QtWidgets.QWidget(parent)
        layout = QtWidgets.QVBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        if column == 4:
            combo = QtWidgets.QComboBox(editor)
            layout.addWidget(combo)
            for version in range(1, 10):
                combo.addItem(f"v{version:03d}")

            slot_changedComboIndex = lambda: self.combo_changed(row_data, combo.currentText(), index)
            combo.currentIndexChanged.connect(slot_changedComboIndex)
        elif column == 5:
            button = QtWidgets.QPushButton(editor)
            layout.addWidget(button)
            button.setText(f"import")
            button.setFixedSize(80, 20)
            labda_button_clicked = lambda : self.btn_func(index=index)
            button.clicked.connect(labda_button_clicked)

        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    @QtCore.Slot()
    def btn_func(self, index):
        self.button_clicked.emit(index)

    @QtCore.Slot()
    def combo_changed(self, row_data: AssetData, version: str, index: QtCore.QModelIndex):
        self.cmb_index_changed.emit(row_data, version, index)