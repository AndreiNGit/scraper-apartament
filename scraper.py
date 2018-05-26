#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import re

def sort(info):
    camere = ""     #Camerele din apartament
    mp = ""         #Mp utili ai apartamentului
    etaj = ""       #Etajul in care se afla apartamentul
    stareBloc = "0" #Starea blocului: nou = 1, vechi = 0
    pret = ""       #Pretul apartamentului
    infoList = info.split() #Converteste sirul intr-o lista folosind ca separator spatiul " "
    for i in range(0, len(infoList)): #Itereaza in fiecare element al listei sirului si preia informatia necesara
        if i == 0:
            if infoList[0] == "o":
                camere = "1"
            else:
                camere = infoList[i];
        elif i == 2:
            if re.search(".", infoList[i]) == None: 
                mp = infoList[i]
            else:
                #sterge punctul dintre cifre pentru a se putea face conversia string-int
                _mp = infoList[i].split(".");
                mp = _mp[0]
        elif i == 6 and infoList[i-1] == "Etaj" or infoList[i-1] == "utili":
            #desparte etajul apartamentului de totalul etajelor
            _etaj = infoList[i].split("/")
            if _etaj[0] == "Parter":
                etaj = "0"
            elif _etaj[0] == "Demisol":
                etaj = "-1"
            else:
                etaj = _etaj[0]
        elif i == len(infoList) - 1:
            #formateaza pretul pentru a se putea face conversia string-int
            if re.search(",", infoList[i]) == None:
                pret = infoList[i].replace(".", "")
            else:
                _pret = infoList[i].split(",")
                pret = _pret[0].replace(".","")
        elif infoList[i] == "nou":
            #daca blocul este nou atunci se modifica variabila 'stareBloc' cu valoarea '1'
            stareBloc = "1"
    row = camere + " " + mp + " " + etaj + " " + stareBloc + " " + pret
    return row;

def scrape(url, fileName):
    page = urllib.request.urlopen(url)
    table = []
    
    html = BeautifulSoup(page, "html.parser")
    
    houseInfo = html.find_all("ul",attrs={"class": "caracteristici"})
    prices = html.find_all("span",attrs={"class": "pret-mare"})
    
    #Portiunea de cod trece prin caracteristicile si preturile fiecarui apartament
    #si le trimite functiei sort pentru a fi prelucrate urmand ca informatia
    #prelucrata sa fie introdusa in lista 'table'
    skipIndex = 0
    for info in houseInfo:
        i = 0
        for price in prices:
            if i < skipIndex: #itereaza pana cand ajunge la pretul corespunzator apartamentului
                i += 1
                continue
            else:
                infoRow = info.text + " " + price.text
                table.append(sort(infoRow))
            break
        skipIndex += 1
    
    #Codul salveaza informatiile din  lista 'table' intr-un fisier
    #cu numele ales de utilizator care se afla in directorul script-ului
    with open(fileName + ".txt", 'a+') as f:
        for row in table:
            f.write(row + "\n")
    
    print("\nDatele apartamentelor au fost salvate in fisierul " + fileName + " sub forma 'camere mp etaj stareBloc pret'")
    
print("Pentru a prelua datele apartamentelor de pe imobiliare.ro folositi functia scrape(\"adresaPagina\", \"numeFisier\")")