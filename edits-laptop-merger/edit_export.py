from PyPDF2 import PdfFileReader, PdfFileWriter,PdfFileMerger
import datetime as dt
from pathlib import Path
import os
import xmltodict



def Find_Pdf(date):
    print("find file")
    test_Fname = "test for arran.pdf"
    
    if int(date.month) < 10:
        month = "0"+str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = "0" + str(date.day)
    else:
        day = str(date.day)
       
    filename =  "pdfs/"+str(date.month) + "/" +str(day)+ str(month)+" mbeb.pdf"
    
    print(filename)
    try:
        pdf = PdfFileReader(str(filename))
    
        print(pdf.getNumPages())
        print("will convert file from pdf to odt for title edit")
    except:
        print("invalid date or no file found")
        pdf = False
    return pdf


def Edit_Pdf(pdf_edit ,date):
    
    pdf_numpages = pdf_edit.getNumPages()
    currentyear = dt.datetime.utcnow()
    removepages = pdf_edit.getNumPages() - (((currentyear.year) - date.year)*2 +2)
    print("removing page 6 though " +  str(removepages))
    print(str(pdf_numpages) +" + "+ str(removepages) +">= "+ str(pdf_numpages))
    if pdf_numpages - removepages >= pdf_numpages - 6:
        print("not enough pages to edit, exporting anyway")
        pdf_writer= PdfFileWriter()
        for n in range(0,pdf_numpages):
            page = pdf_edit.getPage(n)
            pdf_writer.addPage(page)
        return pdf_writer
    else:
        pdf_writer = PdfFileWriter()
        for n in range(0,4):
            page = pdf_edit.getPage(n)
            pdf_writer.addPage(page)
        for n in range(removepages,pdf_numpages):
            page = pdf_edit.getPage(n)
            pdf_writer.addPage(page)

        print( "original pdf lenght "+ str(pdf_numpages)+ " | new PDF length:"+str(pdf_writer.getNumPages()))
        
        return pdf_writer
    

def Export_Pdf(batch_num, ready_pdf,date):
        if not os.path.exists("batches/"+batch_num):
            os.mkdir("batches/" + batch_num)
            print("Making Batch folder, and exporting")
        else:
            print("batch folder already exists exporting to file")
        with Path("batches/"+batch_num,str(date.year)+str(date.month)+str(date.day)+"-Title Edit Required.pdf").open(mode="wb") as output_File:
            ready_pdf.write(output_File)


def AutoRun():  
    for file in os.listdir("batchxml"):
        if file.endswith(".xml"):
            curr_job = readXML(os.path.join("batchxml",file))
            curr_pdf = XML_getPDF(curr_job)
            curr_jobDate = curr_pdf[1]
            curr_pdf = curr_pdf[0]
            curr_pdf = Edit_Pdf(curr_pdf,curr_jobDate)
            Export_Pdf(curr_job["Batch"]["Calendar"]["JobTicket"],curr_pdf,curr_jobDate)

            #os.remove(file)



def readXML(xmlfilepath):  
    with open(xmlfilepath) as fd:
        curr_job = xmltodict.parse(fd.read())
        print(curr_job["Batch"]["Calendar"]["JobTicket"])
    

    return curr_job

def XML_getPDF(data):
    date = data["Batch"]["Calendar"]["StockItem"]
    temp = ""
    for x in range(0,8):
        temp = temp + date[x]
    date = temp
    date = dt.datetime.strptime(date,"%Y%d%m")
    print(date)
    pdf = list()
    pdf.append(Find_Pdf(date))
    pdf.append(date)
    return pdf

print("importing methods")

