import os
import random
import pandas as pd
from PyQt6.QtCore import Qt, QUrl
from collections import Counter
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QLabel, QSpinBox, QHBoxLayout, QCheckBox

from setting import SOURCE_TYPE, DRIVE_LINK, LOCAL_PATH, get_path

class data_handle:
    path = None
    
    chap_sta = None
    chap_content = None
    ques_choose = {"TN":[], "TL":[]}

    def __init__(self,GUI):
        self.chap_tray = {}
        self.GUI = GUI
        self.GUI.content_shower.setColumnCount(6)
        self.GUI.content_shower.setHorizontalHeaderLabels(["Question","Type","Level","Content","Link","Chose"])
        self.GUI.subject_list.currentTextChanged.connect(self.chapter_list_take)
        self.GUI.chap_list.currentTextChanged.connect(self.chapter_load)
        self.GUI.content_shower.itemClicked.connect(self.ques_state_take)
        self.GUI.mode.currentTextChanged.connect(self.mode)
        self.GUI.make.clicked.connect(self.make)

    def begin_load(self):
        if SOURCE_TYPE == "drive":
            self.from_drive()
        elif SOURCE_TYPE == "local":
            self.from_local()
        else:
            raise ValueError("Invalid SOURCE_TYPE specified.")
        
    def from_drive(self):
        # Implement logic to load data from Google Drive using DRIVE_LINK
        pass

    def from_local(self):
        if os.path.exists(LOCAL_PATH):
            self.path = LOCAL_PATH
            folders = [f for f in os.listdir(LOCAL_PATH) if os.path.isdir(os.path.join(LOCAL_PATH, f))]
            self.GUI.subject_list.addItems(folders)
        else:
            self.path = DRIVE_LINK
            print(f"Folder does not exist")

    def chapter_list_take(self):
        self.chap_tray.clear()
        self.GUI.chap_list.blockSignals(True)
        self.GUI.chap_list.clear()
        subject_path = os.path.join(LOCAL_PATH, self.GUI.subject_list.currentText())
        chap_list  = [f for f in os.listdir(subject_path) if os.path.isdir(os.path.join(subject_path, f))]
        self.GUI.chap_list.addItems(chap_list)
        self.chap_tray.update({k: {"chap_content":None, "chap_sta":None, "ques_choose":None} for k in chap_list})
        self.GUI.chap_list.blockSignals(False)

    def chapter_load(self):
        if self.chap_tray[self.GUI.chap_list.currentText()]["chap_content"] is not None:
            print(1111)
            self.chap_content = self.chap_tray[self.GUI.chap_list.currentText()]["chap_content"]
            self.chap_sta = self.chap_tray[self.GUI.chap_list.currentText()]["chap_sta"]
            self.ques_choose = self.chap_tray[self.GUI.chap_list.currentText()]["ques_choose"]
        else:
            print(1112)
            df = pd.read_excel(os.path.join(LOCAL_PATH,self.GUI.subject_list.currentText(),self.GUI.chap_list.currentText(),"question.xlsx"))
            self.chap_content = df.to_dict(orient="records")
            self.chap_sta = self.chap_statictics(self.chap_content)
            self.chap_tray[self.GUI.chap_list.currentText()]["chap_content"] = self.chap_content
            self.chap_tray[self.GUI.chap_list.currentText()]["chap_sta"] = self.chap_sta
            self.ques_choose = {"TN":[], "TL":[]}
            self.chap_tray[self.GUI.chap_list.currentText()]["ques_choose"] = self.ques_choose
        self.chapter_show()
        self.mode()

    def chapter_show(self):
        self.GUI.content_shower.clear()
        self.GUI.TN_table.clear()
        self.GUI.TL_table.clear()
        if self.chap_content:
            self.GUI.content_shower.setRowCount(len(self.chap_content))
            for row_idx, row_data in enumerate(self.chap_content):
                quest = str(row_data['Question'])
                self.GUI.content_shower.setItem(row_idx, 0, QTableWidgetItem(quest.replace("_x000D_", "")))
                self.GUI.content_shower.setItem(row_idx, 1, QTableWidgetItem(str(row_data['Type'])))
                self.GUI.content_shower.setItem(row_idx, 2, QTableWidgetItem(str(row_data['Level'])))
                self.GUI.content_shower.setItem(row_idx, 3, QTableWidgetItem(str(row_data['Content'])))
                self.GUI.content_shower.setItem(row_idx, 4, QTableWidgetItem(str(row_data['Link'])))
                check_item = QTableWidgetItem()
                check_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
                check_item.setCheckState(Qt.CheckState.Unchecked)
                if row_idx in self.ques_choose["TN"] or row_idx in  self.ques_choose["TL"]:
                    check_item.setCheckState(Qt.CheckState.Checked)
                else:
                    check_item.setCheckState(Qt.CheckState.Unchecked)
                self.GUI.content_shower.setItem(row_idx, 5, check_item)
            
            self.GUI.content_shower.resizeColumnsToContents()
            self.GUI.content_shower.resizeRowsToContents()
            self.GUI.content_shower.setColumnWidth(0, 200)

        if self.chap_sta:
            L = len(self.chap_sta["sta"])
            self.GUI.TN_table.setRowCount(L+1)
            self.GUI.TL_table.setRowCount(L+1)
            for row_idx, row_data in enumerate(self.chap_sta["sta"]):
                self.GUI.TN_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data["Content"])))
                self.GUI.TN_table.setCellWidget(row_idx, 1, item(row_data["TN_E"]))
                self.GUI.TN_table.setCellWidget(row_idx, 2, item(row_data["TN_M"]))
                self.GUI.TN_table.setCellWidget(row_idx, 3, item(row_data["TN_H"]))
                self.GUI.TN_table.setCellWidget(row_idx, 4, item(row_data["TN_E"]+row_data["TN_M"]+row_data["TN_H"]))
                self.GUI.TL_table.setItem(row_idx, 0, QTableWidgetItem(str(row_data["Content"])))
                self.GUI.TL_table.setCellWidget(row_idx, 1, item(row_data["TL_E"]))
                self.GUI.TL_table.setCellWidget(row_idx, 2, item(row_data["TL_E"]))
                self.GUI.TL_table.setCellWidget(row_idx, 3, item(row_data["TL_E"]))
                self.GUI.TL_table.setCellWidget(row_idx, 4, item(row_data["TL_E"]+row_data["TL_M"]+row_data["TL_H"]))
            
            self.GUI.TN_table.setItem(L, 0, QTableWidgetItem("Total"))
            self.GUI.TN_table.setCellWidget(L, 1, item(self.chap_sta["E_N"]))
            self.GUI.TN_table.setCellWidget(L, 2, item(self.chap_sta["M_N"]))
            self.GUI.TN_table.setCellWidget(L, 3, item(self.chap_sta["H_N"]))
            self.GUI.TN_table.setCellWidget(L, 4, item(self.chap_sta["E_N"]+self.chap_sta["M_N"]+self.chap_sta["H_N"]))

            self.GUI.TL_table.setItem(L, 0, QTableWidgetItem("Total"))
            self.GUI.TL_table.setCellWidget(L, 1, item(self.chap_sta["E_L"]))
            self.GUI.TL_table.setCellWidget(L, 2, item(self.chap_sta["M_L"]))
            self.GUI.TL_table.setCellWidget(L, 3, item(self.chap_sta["H_L"]))
            self.GUI.TL_table.setCellWidget(L, 4, item(self.chap_sta["E_L"]+self.chap_sta["M_L"]+self.chap_sta["H_L"]))

    def chap_statictics(self,data):
        Con_list = list(Counter(v["Content"] for v in data if "Content" in v).keys())
        sta = []
        E_N = 0
        M_N = 0
        H_N = 0
        E_L = 0
        M_L = 0
        H_L = 0
        for content in Con_list:
            TN = Counter(
                v["Level"] 
                for v in data
                if v["Type"] == "TN" and v["Content"] == content and "Level" in v
            )
            TL = Counter(
                v["Level"] 
                for v in data
                if v["Type"] == "TL" and v["Content"] == content and "Level" in v
            )
            E_N = E_N + TN["E"]
            M_N = M_N + TN["M"]
            H_N = H_N + TN["H"]
            E_L = E_L + TL["E"]
            M_L = M_L + TL["M"]
            H_L = H_L + TL["H"]
            sta.append({"Content": content, "TN_E": TN["E"], "TN_M": TN["M"], "TN_H": TN["H"], "TL_E": TL["E"], "TL_M": TL["M"], "TL_H": TL["H"]})
        return {"sta":sta,"E_N":E_N,"M_N":M_N,"H_N":H_N,"E_L":E_L,"M_L":M_L,"H_L":H_L}
    
    def find_indices(self,data, content, level, type):
        if content == "all":
            return [i for i, v in enumerate(data) if v.get("Level") == level and v.get("Type") == type]
        elif level == "all":
            return [i for i, v in enumerate(data) if v.get("Content") == content and v.get("Type") == type]
        elif type == "all":
            return [i for i, v in enumerate(data) if v.get("Content") == content and v.get("Level") == level]
        else:
            return [i for i, v in enumerate(data) if v.get("Content") == content and v.get("Level") == level and v.get("Type") == type]
    
    def ques_state_take(self,item):
        # Take data of content_show
        print("Item changed")
        print(f"Row: {item.row()}, Column: {item.column()}, Text: {item.text()}")
        if item.column() == 5:
            try:
                if self.chap_content[item.row()]["Type"] == "TN":
                    if item.checkState() == Qt.CheckState.Checked:
                        if item.row()  not in self.ques_choose["TN"]:
                            self.ques_choose["TN"].append(item.row())
                    else:
                        if item.row()  in self.ques_choose["TN"]:
                            self.ques_choose["TN"].remove(item.row())
                if self.chap_content[item.row()]["Type"] == "TL":
                    if item.checkState() == Qt.CheckState.Checked:
                        if item.row()  not in self.ques_choose["TL"]:
                            self.ques_choose["TL"].append(item.row())
                    else:
                        if item.row()  not in self.ques_choose["TL"]:
                            self.ques_choose["TL"].remove(item.row())
            except Exception as e:
                print(e)
            self.chap_tray[self.GUI.chap_list.currentText()]["ques_choose"] = self.ques_choose
            print(self.chap_tray)
            print(self.chap_tray[self.GUI.chap_list.currentText()]["ques_choose"])
            print("DATA id:", id(self.chap_tray))
        if item.column() == 4:
            try:
                path = os.path.join(self.path,self.GUI.subject_list.currentText(),
                                    self.GUI.chap_list.currentText(),'image',item.text())
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            except Exception as e:
                print(e)
                pass

    def mode(self): #Enable table cell according to mode
        TN_r = self.GUI.TN_table.rowCount()-1
        TL_r = self.GUI.TL_table.rowCount()-1
        def set_spin_enable(table,p1,p2,p3,p4):
            row = table.rowCount()
            col = table.columnCount()
            for r in range(row):
                for c in range(col):
                    item = table.cellWidget(r, c)
                    if item is not None:
                        if (p1 <= r <= p2) and (p3 <= c <= p4):
                            item.spin.setEnabled(True)
                        else:
                            item.spin.setEnabled(False)

        if self.GUI.mode.currentText() == "Combine":
            set_spin_enable(self.GUI.TN_table,0,TN_r-1,1,3)
            set_spin_enable(self.GUI.TL_table,0,TL_r-1,1,3)

        if self.GUI.mode.currentText() == "Level":
            set_spin_enable(self.GUI.TN_table,TN_r,TN_r,1,3)
            set_spin_enable(self.GUI.TL_table,TL_r,TL_r,1,3)

        if self.GUI.mode.currentText() == "Content":
            set_spin_enable(self.GUI.TN_table,0,TN_r-1,4,4)
            set_spin_enable(self.GUI.TL_table,0,TL_r-1,4,4)

    def make(self):
        print("Make function called")
        data = self.chap_tray[self.GUI.chap_list.currentText()]["chap_content"]
        self.ques_choose = {"TN":[], "TL":[]}
        TN_r = self.GUI.TN_table.rowCount()
        TL_r = self.GUI.TL_table.rowCount()
        TN_idx = []
        TL_idx = []
        if self.GUI.mode.currentText() == "Combine":
            for i in range(TN_r-1):
                content = self.GUI.TN_table.item(i,0).text()
                E_count = self.GUI.TN_table.cellWidget(i,1).spin.value()
                M_count = self.GUI.TN_table.cellWidget(i,2).spin.value()
                H_count = self.GUI.TN_table.cellWidget(i,3).spin.value()
                E_indices = self.find_indices(data, content, "E", "TN")
                M_indices = self.find_indices(data, content, "M", "TN")
                H_indices = self.find_indices(data, content, "H", "TN")
                TN_idx += random.sample(E_indices, E_count) + random.sample(M_indices, M_count) + random.sample(H_indices, H_count)
            for i in range(TL_r-1):
                content = self.GUI.TL_table.item(i,0).text()
                E_count = self.GUI.TL_table.cellWidget(i,1).spin.value()
                M_count = self.GUI.TL_table.cellWidget(i,2).spin.value()
                H_count = self.GUI.TL_table.cellWidget(i,3).spin.value()
                E_indices = self.find_indices(data, content, "E", "TL")
                M_indices = self.find_indices(data, content, "M", "TL")
                H_indices = self.find_indices(data, content, "H", "TL")
                TL_idx += random.sample(E_indices, E_count) + random.sample(M_indices, M_count)  + random.sample(H_indices, H_count)

        if self.GUI.mode.currentText() == "Level":
            E_count = self.GUI.TN_table.cellWidget(TN_r-1,1).spin.value()
            M_count = self.GUI.TN_table.cellWidget(TN_r-1,2).spin.value()
            H_count = self.GUI.TN_table.cellWidget(TN_r-1,3).spin.value()
            E_indices = self.find_indices(data, "all", "E", "TN")
            M_indices = self.find_indices(data, "all", "M", "TN")
            H_indices = self.find_indices(data, "all", "H", "TN")
            TN_idx = (random.sample(E_indices, E_count) + random.sample(M_indices, M_count)  + random.sample(H_indices, H_count))

            E_count = self.GUI.TL_table.cellWidget(TL_r-1,1).spin.value()
            M_count = self.GUI.TL_table.cellWidget(TL_r-1,2).spin.value()
            H_count = self.GUI.TL_table.cellWidget(TL_r-1,3).spin.value()
            E_indices = self.find_indices(data, "all", "E", "TL")
            M_indices = self.find_indices(data, "all", "M", "TL")
            H_indices = self.find_indices(data, "all", "H", "TL")
            TL_idx = (random.sample(E_indices, E_count) + random.sample(M_indices, M_count)  + random.sample(H_indices, H_count))

        if self.GUI.mode.currentText() == "Content":
            for i in range(TN_r-1):
                content = self.GUI.TN_table.item(i,0).text()
                total = self.GUI.TN_table.cellWidget(i,4).spin.value()
                indices = self.find_indices(data, content, "all", "TN")
                TN_idx += random.sample(indices, total)

            for i in range(TL_r-1):
                content = self.GUI.TL_table.item(i,0).text()
                total = self.GUI.TL_table.cellWidget(i,4).spin.value()
                indices = self.find_indices(data, content, "all", "TL")
                TL_idx += random.sample(indices, total)
        
        self.ques_choose["TN"] = TN_idx
        self.ques_choose["TL"] = TL_idx
        self.chap_tray[self.GUI.chap_list.currentText()]["ques_choose"] = self.ques_choose
        print(self.chap_tray[self.GUI.chap_list.currentText()]["ques_choose"])

        row_count = self.GUI.content_shower.rowCount()

        self.GUI.content_shower.blockSignals(True)
        for i in range(row_count):
            check_item = QTableWidgetItem()
            check_item.setFlags(
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsUserCheckable
            )

            if i in self.ques_choose["TN"] or i in self.ques_choose["TL"]:
                check_item.setCheckState(Qt.CheckState.Checked)
            else:
                check_item.setCheckState(Qt.CheckState.Unchecked)

            self.GUI.content_shower.setItem(i, 5, check_item)
        self.GUI.content_shower.blockSignals(False)

class item(QWidget):
    def __init__(self, display_value=0, input_value=0, parent=None):
        super().__init__(parent)

        self.label = QLabel(str(display_value))
        self.spin = QSpinBox()

        self.spin.setRange(0, display_value)
        self.spin.setValue(input_value)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.spin)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(1)