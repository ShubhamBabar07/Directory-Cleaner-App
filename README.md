

	Project Name : Directory Automation with Auto Scheduled Log Report Facility
  Technology : Python
  

  Description:
	Designed automation script which performs following task.
 
  Accept Directory name from user and delete all duplicate files from the specified directory by
	considering the checksum of files.

	Create one Directory named as Demo and inside that directory create log file which 
	maintains all names of duplicate files which are deleted.

	Name of that log file contains the date and time at which that file gets created.

	Accept duration in minutes from user and perform task of duplicate file removal after the specific 
	time interval.

	Accept Mail id from user and send the attachment of the log file.

	Mail body contains statistics about the operation of duplicate file removal.

	Mail body contains below things:
		Starting time of scanning
		Total number of files scanned
		Total number of duplicate files found

	Consider below command line options for the script
	Duplicate FileRemoval.py E:/Data/Demo 50 SomeMail@gmail.com
