import os
import re
import time

import xlrd
import sqlite3

from excel_tools import col_name


# tidsmåling
start = time.time()

# instillinger
sti_til_reletabeller = r"C:\Users\weyhak\OneDrive - Bane NOR\Dokumenter\Tools\Python\testtabeller\komplett"
# dbName = ":memory:"
dbName = r"C:\Users\weyhak\OneDrive - Bane NOR\Dokumenter\Tools\Python\rele77.db"

# variabler til DB
rtabID = 0
releID = 0
kontaktID = 0

rtabList = []
releList = []
kontaktList = []

# variabler til søk
rtab_col = ["X", "AL", "AZ", "BN", "CB", "CP", "DD", "DR", "EF", "ET"] # hvilke kolonner det skal søkes i
search_columns = [col_name(letter) for letter in rtab_col]
search_rows = range(0,26) # søker fra rad 1 til og med rad 26

reletype_besetning = {
        "RE 1010" : [10, 10],
        "RE 0810" : [12, 8],
        "RE 0301" : [17, 3],
        "RE 0501" : [15, 5],
        "RE 0704" : [13, 7],
        "RE 1004" : [10, 10],
        "RD 0521" : [5, 5],
        "RD 0210" : [8, 2],
        "RD 0310" : [7, 3],
        "RD 0409" : [6, 4],
        "RD 0508" : [5, 5],
        "RD 0405" : [6, 4],
        "RD 0507" : [5, 5],
        "RC 0215" : [4, 2],
        "RC 0323" : [3, 3],
        "RC 0326" : [3, 3],
        "RC 0226" : [4, 2],
        "RC 0232" : [4, 2],
        "RC 0331" : [3, 3],
        "RC 0430" : [2, 4],
        "RC 0229" : [4, 2],
        "RC 0223" : [4, 2],
        "PE 0908" : [10, 9],
        "PD 0502" : [4, 5],
        "PD 0308" : [99, 99],
        "FD 0086" : [6, 2]
        }

##############
# funksjoner #
##############

def hent_kontakter(row, kontaktID, colOffset=7):
    # hente F-kontakter
    row += 1
    kontaktNummer = reletype_besetning[key][0] + reletype_besetning[key][1]
    for j in range(reletype_besetning[key][0]): # for-kontakter
        if wb_sheet.cell(row, col).ctype==1:
            # print(row, "F{}: {}" .format(kontaktNummer, wb_sheet.cell_value(row, col).replace("\n", "")))
            kontaktList.append((
                kontaktID, # kontaktID INTEGER,
                releID, # releID INTEGER,
                "F", # for_bak,
                kontaktNummer, # kontaktnr,
                wb_sheet.cell_value(row, col).replace("\n", "") # snr,
            ))
            kontaktID += 1
        else:
            # print(row, "(tom)")
            pass
        row += 1
        kontaktNummer -= 1

    # hente B-kontakter
    kontaktNummer = reletype_besetning[key][1]
    for j in range(reletype_besetning[key][1]): # bak-kontakter
        if wb_sheet.cell(row, col + colOffset).ctype==1:
            # print(row, "B{}: {}" .format(kontaktNummer, wb_sheet.cell_value(row, col + colOffset).replace("\n", "")))
            kontaktList.append((
                kontaktID, # kontaktID INTEGER,
                releID, # releID INTEGER,
                "B", # for_bak,
                kontaktNummer, # kontaktnr,
                wb_sheet.cell_value(row, col).replace("\n", "") # snr,
            ))
            kontaktID += 1
        else:
            # print(row, "(tom)")
            pass
        row += 1
        kontaktNummer -= 1

    return kontaktID


###########
# program #
###########

# søke gjennom mappe
reletabeller = []
(_, _, filenames) = next(os.walk(sti_til_reletabeller))

# for file in filenames:
#     if file.lower().endswith(".xls"):
#         reletabeller.append(sti_til_reletabeller + "\\" + file)

xls_filer = [sti_til_reletabeller + "\\" + file for file in filenames if file.lower().endswith(".xls")]
print("Antall .XLS-filer funnet: {}" .format(len(xls_filer)))
xlsx_filer = [sti_til_reletabeller + "\\" + file for file in filenames if file.lower().endswith(".xlsx")]
print("Antall .XLSX-filer funnet: {}" .format(len(xlsx_filer)))
reletabeller = xls_filer + xlsx_filer
# input("Trykk ENTER tast for å fortsette...")


# åpne fil og skrive db
for reletabell in reletabeller:
    print(reletabell)      
    wbook = xlrd.open_workbook(reletabell) # åpner excel workbook
    wb_sheet = wbook.sheet_by_index(0) # aktiverer sheet nr 0

    snr = str(wb_sheet.cell_value(39, col_name("EF"))) # snr
    if re.match("S.[0-9]{6}", snr) is None: # ser i relevant celle etter snr
        print("Ikke en reletabell? ", snr)
    else:
        rtabList.append((
            rtabID,
            str(wb_sheet.cell_value(39, col_name("EF"))), # snr
            str(wb_sheet.cell_value(36, col_name("DF"))), # ramme
            str(wb_sheet.cell_value(36, col_name("DR"))) # seksjon
        ))
        

        # ramme = str(wb_sheet.cell_value(36, col_name("DF"))) # ramme
        # seksjon = str(wb_sheet.cell_value(36, col_name("DR"))) # seksjon
        # snr = str(wb_sheet.cell_value(39, col_name("EF"))) # snr
    

    # finne rele og skrive db
    for col in search_columns:
        iter_rows = iter(search_rows)            
        for row in iter_rows:
            # inneholder cellen et s-nr?
            if re.match("S.[0-9]{6}", str(wb_sheet.cell_value(row, col))):
                # ligner cellen to rader under på et relenavn?
                if re.match("[A-Z]{2} *[0-9]{4}", wb_sheet.cell_value(row + 2, col)):
                    # hvis ja, kopier
                    reletype = wb_sheet.cell_value(row + 2, col)
                    relesignatur = wb_sheet.cell_value(row + 4, col).replace("\n", " ")
                    releList.append((
                        releID,
                        rtabID,
                        relesignatur,
                        reletype,
                        str(wb_sheet.cell_value(row, col)), # spole_nr
                        row,
                        col
                    ))

                    # finne kontakter og skrive db
                    for key in reletype_besetning:
                        if key == reletype:
                            # print()
                            # print(relesignatur)
                            # print(reletype)
                            if row == 0 and wb_sheet.cell_value(row + 5, col) == "F":
                                kontaktID = hent_kontakter(row + 5, kontaktID)
                            else:
                                kontaktID = hent_kontakter(row + 7, kontaktID)
                            break
                    releID += 1
    rtabID += 1

# opprette db
conn = sqlite3.connect(dbName)
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

c.execute('''
    CREATE TABLE reletabeller(
        rtabID INTEGER,
        snr,
        ramme,
        seksjon,
        PRIMARY KEY(rtabID ASC)
        );
    ''')

c.execute('''
    CREATE TABLE releer(
        releID INTEGER,
        rtabID INTEGER,
        signatur,
        type,
        spole_snr,
        rtab_row,
        rtab_col,
        PRIMARY KEY(releID ASC),
        FOREIGN KEY(rtabID) REFERENCES reletabeller(rtabID)
        );
    ''')

c.execute('''
    CREATE TABLE kontakter(
        kontaktID INTEGER,
        releID INTEGER,
        for_bak,
        kontaktnr,
        snr,
        PRIMARY KEY(kontaktID ASC),
        FOREIGN KEY(releID) REFERENCES releer(releID)
        );
    ''')


if len(rtabList) > 0:
    c.executemany("INSERT INTO reletabeller VALUES ({})" .format("?," * (len(rtabList[0])-1) + "?"), rtabList)
    c.executemany("INSERT INTO releer VALUES ({})" .format("?," * (len(releList[0])-1) + "?"), releList)
    c.executemany("INSERT INTO kontakter VALUES ({})" .format("?," * (len(kontaktList[0])-1) + "?"), kontaktList)

# avslutte db
conn.commit()
conn.close()

# oppsummering
print("Antall releer funnet: {}" .format(len(releList)))
print("Runtime: {0:.2f} s" .format(time.time() - start))

"""
SELECT kontakter.snr, releer.signatur, kontakter.for_bak, kontakter.kontaktnr
FROM kontakter
INNER JOIN releer ON kontakter.releID=releer.releID

Antall releer per reletabell:
SELECT reletabeller.snr, COUNT(releer.signatur)
FROM reletabeller
INNER JOIN releer ON reletabeller.rtabID=releer.rtabID
GROUP BY reletabeller.snr
ORDER BY COUNT(releer.signatur)

Antall kontakter per rele
SELECT releer.signatur, count(kontakter.kontaktID) as 'Antall'
FROM releer
INNER JOIN kontakter ON releer.releID = kontakter.releID
GROUP BY releer.signatur
ORDER BY count(kontakter.kontaktID)
"""