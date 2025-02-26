# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 14:12:29 2022

@author: Fatih
"""

#------------------------KÜTÜPHANE------------------------
import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *

#----------------------UYGULAMA OLUŞTUR------------------
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

#---------------------VERİTABANI OLUŞTUR-------------
import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabani.db')
curs=conn.cursor()
sorguCreTblAlasim=("CREATE TABLE IF NOT EXISTS alasim(            \
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,           \
    Malzeme TEXT NOT NULL UNIQUE,                            \
    Uzunluk INTEGER NOT NULL,                                \
    Alan INTEGER NOT NULL)")
curs.execute(sorguCreTblAlasim)
conn.commit()
                  
#-----------------EKLE--------------------------
#-----------------------------------------------
def EKLE():
    _CBmadde=ui.CBmadde.currentText()
    _LEuzun=ui.LEuzun.text()
    _LEalan=ui.LEalan.text()
    curs.execute("INSERT INTO alasim \
                  (Malzeme,Uzunluk,Alan) \
                      VALUES (?,?,?)", \
                          (_CBmadde,_LEuzun,_LEalan))
    conn.commit()
    LISTELE()
#-------------LİSTELE-------------
#----------------------------------
def LISTELE():
    ui.TWalasim.clear()
    ui.TWalasim.setHorizontalHeaderLabels(('No','Malzeme','Uzunluk','Alan'))
    ui.TWalasim.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM alasim")
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.TWalasim.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.CBmadde.setCurrentIndex(-1)
    ui.LEalan.clear()
    ui.LEuzun.clear()
    
    curs.execute("SELECT COUNT(*) FROM alasim")
    kayitsayisi = curs.fetchone()
    ui.LBpdeger.setText(str(kayitsayisi[0]))
    
    
    
    
    
    
LISTELE()

#-----------------SİL-----------------------
#--------------------------------------------
def SIL():
    cevap=QMessageBox.question(penAna,"TEMİZLE","Kaydı silmek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.TWalasim.selectedItems()
        silinecek=secili[1].text()
        try:
            curs.execute("DELETE FROM alasim WHERE Malzeme='%s'" %(silinecek))
            conn.commit()
            
            LISTELE()
            
            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...",10000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi...",10000)


#-----------------HESAPLAMA----------------------------
#----------------------------------------------------
def HESAPLA():
    
    listeU=[]
    curs.execute("SELECT Uzunluk FROM alasim ")
    for i in curs.fetchall():
        listeU.append(i[0])
    
    listeA=[]
    curs.execute("SELECT Alan FROM alasim ")
    for i in curs.fetchall():
        listeA.append(i[0])
    
    
    listeK=[]
    curs.execute("SELECT katsayi FROM madde, alasim WHERE alasim.Malzeme = madde.malzeme ")
    for i in curs.fetchall():
        listeK.append(i[0])

    
    
#1, FORMÜL UZAMA:
    curs.execute("SELECT COUNT(*) FROM alasim")
    kayitsayisi = curs.fetchone()
   
    a=0
    b=0
    um=0
    for i in range(kayitsayisi[0]):
        b= ((a+1)*listeU[a])/(listeA[a]*listeK[a])
        a=a+1
        um=um+b
    ui.LBumd.setText(str(um))    
    
#2. FORMÜL GERİLME
    a=0
    b=0
    gm=0
    for i in range(kayitsayisi[0]):
        b= (a+1)/listeA[a]
        a=a+1
        gm=gm+b
    ui.LBgmd.setText(str(gm))
    
#3.FORMÜL BİRİM ŞEKİL DEĞİŞTİRME
    a=0
    b=0
    bsd=0
    for i in range(kayitsayisi[0]):
        b= um/listeU[a]
        a=a+1
        bsd=bsd+b
    ui.LBbsdmd.setText(str(bsd))    
      
HESAPLA()    
    
  

#-------------------sinyal-slot------------
#--------------------------------------------
ui.PBekle.clicked.connect(EKLE)
ui.PBekle.clicked.connect(LISTELE)
ui.PBtemiz.clicked.connect(SIL)
ui.PBhesapla.clicked.connect(HESAPLA)




sys.exit(Uygulama.exec_())
