import PyPDF2
# import traceback
from pathlib import Path
import re


def makeTime(x):
    # tar en dato formatert som en str og konverterer til datetime obj
    # eks: D:20190122135319+01'00'
    from datetime import datetime
    try:
        dt_obj = datetime(
                        int(x[2:6]),
                        int(x[6:8]),
                        int(x[8:10]),
                        int(x[10:12]),
                        int(x[12:14]),
                        int(x[14:16])
                    )
    except:
        print("datetime() error")
    return dt_obj

def browseFolder(folderPath):
    filePathList = list(Path(folderPath).glob("*.pdf"))
    print(f"Antall .pdf-filer funnet: {len(filePathList)}")
    return filePathList

def split_doc_filename(filename):
    search_pattern = "[A-Z]{3}.[0-9]{2}.[A-Z].[0-9]{5}_[0-9]{2}[A-Z]{1}"
    m = re.search(search_pattern, filename, re.I)
    if m:
        docNr = m.string[0:14]
        docRev = m.string[15:18]
        return docNr, docRev
    else:
        print(f"No valid document number and revision in \"{filename}\"")
        return "?", "?"


myFolder = r"C:\Users\weyhak\Desktop\temp\Ny mappe"

for filePath in browseFolder(myFolder):
    input1 = PyPDF2.PdfFileReader(open(filePath, "rb"))
    nPages = input1.getNumPages()

    for i in range(nPages) :
        page0 = input1.getPage(i)
        try :
            for annot in page0['/Annots'] :
                objectX = annot.getObject()
                try:
                    if objectX["/Contents"] != "":
                        docNr, docRev = split_doc_filename(filePath.stem)
                        cDate = makeTime(objectX["/CreationDate"])
                        # print("{};{};{};{}" .format(filePath[(len(myFolder)+1):-4], objectX["/T"], cDate, objectX["/Contents"])) # (1)
                        print(f"{objectX['/Contents']};;{docNr};{docRev};;{cDate};{objectX['/T']}")
                except:
                    # no contents
                    pass
        except : 
            # there are no annotations on this page
            # print("Ingen kommentar")
            pass