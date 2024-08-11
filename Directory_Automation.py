# Designed automation script which performs following task.
# Accept Directory name from user and delete all duplicate files from the specified directory by
# considering the checksum of files.
# Create one Directory named as Demo and inside that directory create log file which 
# maintains all names of duplicate files which are deleted.
# Name of that log file contains the date and time at which that file gets created.
# Accept duration in minutes from user and perform task of duplicate file removal after the specific 
# time interval.
# Accept Mail id from user and send the attachment of the log file.
# Mail body contains statistics about the operation of duplicate file removal.
# Mail body contains below things:
# 	Starting time of scanning
# 	Total number of files scanned
# 	Total number of duplicate files found
# Consider below command line options for the gives script
#   Duplicate FileRemoval.py E:/Data/Demo 50 SomeMail@gmail.com


from sys import *
import os
import hashlib
import time
import schedule
import urllib3
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def is_connected():
    try:
        urllib3.connectionpool.connection_from_url('http://216.58.192.142', timeout = 1)
        return True
    
    except urllib3.urlError as err:
        return False
    
    except Exception as E:
        print("Error : Not Connected",E)


def MailSender(filename, time, ToMail, FilesScanned, FilesDeleted):
    try:
        fromAddr = "ABC@gmail.com"      # from address
        toAddr = ToMail                 # To address

        msg = MIMEMultipart()

        msg['From'] = fromAddr
        msg['To'] = toAddr

        body = """
                Hello %s,

                Please find attached document which contains Log of Duplicate Files.
                Log file is created at : %s
                Total files Scanned : %s
                Total Duplicate files deleted : %s

                This is Auto-Generated mail.
                
                Thanks and Regards
                """%(toAddr, time, FilesScanned, FilesDeleted)
        
        subject = """ Directory Cleaner Log Generated at : %s""" %(time)
        
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, 'rb')

        p =MIMEBase('application', 'octet-stream')

        p.set_payload((attachment).read())

        encoders.encode_base64(p)

        p.add_header('Content-Deposition',"attachment; filename = %s" %(filename))

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com',587)

        s.starttls()

        s.login(fromAddr, "-----------")  # password

        text = msg.as_string()

        s.sendmail(fromAddr, toAddr, text)

        s.quit()

        print("Log file successfully send throgh mail")

    except Exception as E:
        print("Unable to send mail ",E)


def DeleteFiles(dict):

    results = list(filter(lambda x : len(x) > 1, dict.values()))

    icnt = 0
    FilesDeleted = 0       # deleted files count

    if len(results) > 0:
        for result in results:
            for subresult in result:
                icnt = icnt + 1
                if icnt >= 2:
                    os.remove(subresult)
                    FilesDeleted = FilesDeleted + 1
                    
            icnt = 0

    return FilesDeleted


def hashfile(path, blocksize = 1024):

    afile = open(path, "rb")
    hasher = hashlib.md5()

    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)

    afile.close()
    return hasher.hexdigest()


def FindDup(path):

    flag = os.path.isabs(path)
    if(flag == False):
        path = os.path.abspath(path)

    exists = os.path.isdir(path)

    FilesScanned = 0

    dups = {}
    if exists:
        for dirname, subdirs, filelist in os.walk(path):

            for filen in filelist:
                path = os.path.join(dirname, filen)
                file_hash = hashfile(path)

                FilesScanned = FilesScanned + 1     # Total files scanned

                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]

        return dups,FilesScanned
                
    else:
        print("Invalid Path")


def CreatingLog(dict):

    separator = "-"*80
    timestamp = time.ctime()
    timestamp = timestamp.replace(" ", "_")
    timestamp = timestamp.replace(":", "-")
    timestamp = timestamp.replace("/", "_")

    FileName = ("DirCleanerLog %s.log"%timestamp)

    fd = open(("DirCleanerLog %s.log"%timestamp), "w")
    fd.write(separator + '\n')
    fd.write("Directory Duplicates log file Created at : "+time.ctime() + '\n')
    fd.write(separator + '\n')

    results = list(filter(lambda x : len(x) > 1, dict.values()))

    if len(results) > 0:
        fd.write("Duplicates Found" + "\n")
        fd.write("The Following files are Duplicates" + "\n")

        icnt = 0
        for result in results:
            for subresult in result:
                icnt = icnt + 1
                if icnt >= 2:
                    fd.write("%s" % subresult + "\n")
                
            icnt = 0

    else:
        fd.write("No Duplicate files found" + "\n")

    fd.write(separator + "\n")
    fd.close()

    return FileName


def CleanerAutomation():
    try:
        arr = {}
        startTime = time.ctime() 

        arr, FilesScanned = FindDup(argv[1])

        FileName = CreatingLog(arr)

        FilesDeleted = DeleteFiles(arr)

        MailSender(FileName, startTime, argv[3], FilesScanned, FilesDeleted )

        print("Log file is created at : %s" %startTime)
        print("Total files Scanned : %s" %FilesScanned)
        print("Total Duplicate files deleted : %s" %FilesDeleted)


    except ValueError:
        print("Error - Invalid Datatype of Input")

    except Exception as E:
        print("Error - Invalid Input",E)


def main():

    print("-------------------------- Directory Automation --------------------------")

    if(len(argv) != 4):
        print("Error - Invalid number of Arguments")
        exit()
    
    if((argv[1] == "--h") or (argv[1] == "--H")):
        print("This is Script is used to traverse specific directory and Delete Duplicates of files")
        exit()
    
    if((argv[1] == "--u") or (argv[1] == "--U")):
        print("Usage : ApplicationName Absolute_Path_Of_Directory Time Mail_Id")
        exit()

    try:
        schedule.every(int(argv[2])).minutes.do(CleanerAutomation)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("Error : Invalid DataType of Input")

    except Exception as E:
        print("Error : Invalid Input ",E)


if __name__ == "__main__":
    main()