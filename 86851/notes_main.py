#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QVBoxLayout,QMessageBox,QRadioButton,QHBoxLayout,QGroupBox,QButtonGroup,QListWidget,QTextEdit,QLineEdit,QInputDialog
import json
my_app=QApplication([])
win=QWidget()
zam=QTextEdit()
l1=QLabel("Список заметок")
list1=QListWidget()
b1=QPushButton("Создать заметку")
b2=QPushButton("Удалить заметку")
b3=QPushButton("Сохранить заметку")
l2=QLabel("Список тегов")
list2=QListWidget()
lineed=QLineEdit()
b4=QPushButton("Добавить к заметке")
b5=QPushButton("Открепить от заметки")
b6=QPushButton("Искать заметки по тегу")
mainlay=QHBoxLayout()
#главный лейаут
lay1=QVBoxLayout()
lay2=QVBoxLayout()
lay3=QHBoxLayout()
lay4=QHBoxLayout()
lay1.addWidget(zam)
lay2.addWidget(l1)
lay2.addWidget(list1)
lay3.addWidget(b1)
lay3.addWidget(b2)
lay2.addLayout(lay3)
lay2.addWidget(b3)
lay2.addWidget(l2)
lay2.addWidget(list2)
lay2.addWidget(lineed)
lay4.addWidget(b4)
lay4.addWidget(b5)
lay2.addLayout(lay4)
lay2.addWidget(b6)
mainlay.addLayout(lay1)
mainlay.addLayout(lay2)
win.setLayout(mainlay)
notes={"Добро пожаловать":{"текст":"привет","теги":["я","ты"]},"Тест":{"текст":"тестовый тест","теги":["тест","не тест"]}}
with open ("notes.json","w",encoding="utf-8") as file :
    json.dump(notes,file,ensure_ascii=False)
def show_note () :
    name=list1.selectedItems()[0].text()
    zam.setText(notes[name]["текст"])
    list2.clear()
    list2.addItems(notes[name]["теги"])
def add_note () :
    note_name,ok=QInputDialog.getText(win,"Добавить заметку","Название заметки:")
    if ok and note_name !="":
        notes[note_name]={"текст":"","теги":[]}
        list1.addItem(note_name)
        #list2.addItems(notes[note_name]["теги"])
def save_note () :
    if list1.selectedItems() :
        key=list1.selectedItems()[0].text()
        notes[key]["текст"]=zam.toPlainText()
        with open("notes.json","w",encoding="utf-8") as file :
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else :
        print("Заметка для сохранения не выбрана")
def del_note() :
    if list1.selectedItems() :
        key=list1.selectedItems()[0].text()
        del notes[key]
        list1.clear()
        list2.clear()
        zam.clear()
        list1.addItems(notes)
        with open("notes.json","w",encoding="utf-8") as file :
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else :
        print("Заметка для удаления не найдена")
def  add_tag () :
    if list1.selectedItems() :
        key=list1.selectedItems()[0].text()
        tag=lineed.text()
        if not tag in notes[key]["теги"] :
            notes[key]["теги"].append(tag)
            list2.addItem(tag)
            lineed.clear()
        with open("notes.json","w",encoding="utf-8") as file :
            json.dump(notes,file,sort_keys=True)
    else :
        print("Заметка для добавления не выбрана!")
def del_tag () :
    if list1.selectedItems() and list2.selectedItems() :
        key=list1.selectedItems()[0].text()
        tag=list2.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list2.clear()
        list2.addItems(notes[key]["теги"])
        with open("notes.json","w",encoding="utf-8") as file :
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print("Тег для удаления не выбран")
def search_tag ():
    tag = lineed.text()
    if b6.text()=="Искать заметки по тегу" and tag :
        notes_filt={}
        for note in notes:
            if tag in notes[note]["теги"] :
                notes_filt[note]=notes[note]
        list1.clear()   
        list2.clear()
        list1.addItems(notes_filt)
        b6.setText("Сбросить поиск")
    elif b6.text()=="Сбросить поиск" :
        list1.clear()
        lineed.clear()
        list2.clear()
        list1.addItems(notes)
        b6.setText("Искать заметки по тегу")
b1.clicked.connect(add_note)
b2.clicked.connect(del_note)
b3.clicked.connect(save_note)
b4.clicked.connect(add_tag)
b5.clicked.connect(del_tag)
b6.clicked.connect(search_tag)
list1.itemClicked.connect(show_note)
with open ("notes.json","r",encoding="utf-8") as file :
    data=json.load(file)
list1.addItems(notes)
win.show()
my_app.exec_()