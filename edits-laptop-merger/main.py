
import re
import datetime as dt
import os
import sys
from edit_export import Edit_Pdf, Export_Pdf, AutoRun, readXML, XML_getPDF


job_done = False


batch_list = ""




while job_done != True:
    batch_number = ""
    if len(sys.argv) < 2:
        batch_number = input("Following commands:\nType digits of the manual batch,\nType 'auto' for automatically running xml\nOr type 'quit' to exit\n")
    curr_batch = batch_number
    if  len(sys.argv) >  1 or batch_number == "auto" :

            AutoRun()
        
    elif batch_number == "quit":
        print("completed batches: " + batch_list)
        job_done = True
    elif batch_number.isdigit() == True:
        while curr_batch == batch_number:
            waiting = True

            curr_job= input("what is the day, month, and year(format = DD/MM/YYYY)? \n")
            #try:
            if True:     
                print(curr_job)
                curr_jobDate = dt.datetime.strptime(curr_job, "%d/%m/%Y")
                curr_pdf = edit_export.Find_Pdf(curr_jobDate)
                if curr_pdf != False:
                    curr_pdf = edit_export.Edit_Pdf(curr_pdf, curr_jobDate)
                    if curr_pdf != False:
                        edit_export.Export_Pdf(curr_batch,curr_pdf,curr_jobDate)
                    while waiting == True:
                        status = input("Add more to this batch? Y/N  ")
                        if status == "N" or status == "n":
                            batch_number = ""
                            batch_list = batch_list + "," + curr_batch
                            waiting = False
                        if status == "y" or status == "Y":
                            print("new file")
                            waiting = False
                else:
                    print("please use a new date")
            #except:
            else:
                print("invaild date, please try again.")

        
    

