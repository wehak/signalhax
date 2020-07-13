# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:49:39 2019

@author: WEYHAK

script for å finne ulikheter mellom to tegningslister

"""

import re
import win32clipboard

##########
# config #
##########

separator = "," # hvilken separator som skal brukes i output-streng
doknr = "[A-Z]{3}-[0-9]{2}-[A-Z]-[0-9]{5}"  # leter etter prosjektnr, feks MIP-00-A-12345


############
# function #
############

def get_document_set():
    while True:
        # instruksjoner til bruker
        print("Kopiér kolonne fra Excel. Data hentes i fra utklippstavlen.")
        input("ENTER for å fortsette ...")
        
        # input hentes fra utklippstavle
        win32clipboard.OpenClipboard()
        input_str = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # finner alle tegningsnr. med regular expressions        
        doknr_list = re.findall(doknr, input_str, re.I)

        print(doknr_list)
        
        # konverterer liste til sett for å fjerne dupliserte verider
        if len(doknr_list) > 0:
            print("{} verdier funnet ({} unike)" .format(len(doknr_list), len(set(doknr_list))))
            print("")
            return set(doknr_list)
        else:
            print("Ingen verdier funnet.")


############
# program #
############

# henter 2 tegingslister fra bruker
print("TEGNINGSLISTE 'A'")
liste_A = get_document_set()
print("TEGNINGSLISTE 'B'")
liste_B = get_document_set()

# finner og printer nummer som ikke finnes i begge
forskjell = liste_B.difference(liste_A)
print("{} tegning(er) fra B finnes ikke i A:" .format(len(forskjell)))
print(separator.join(forskjell))
print("")

forskjell = liste_A.difference(liste_B)
print("{} tegning(er) fra A finnes ikke i B:" .format(len(forskjell)))
print(separator.join(forskjell))
print("")


# unngå at terminal lukkes umiddelbart
print("*******************")
input("Trykk ENTER for å avslutte")
