# ImageFileWrapper.py
# by Allan Niemerg 12 January 2013
# This class is meant to access and manipulate PAIR Image File Wrappers
# It is configured to use already downloaded files or to access and download the
# file wrapper from Google. The downloaded file will be placed in the current working directory 
# and will be retained upon the end of the class. All extracted files will be deleted. 

import urllib2
import shutil
import zipfile
import os
from os.path import expanduser


class ImageFileWrapper:
	def __init__(self, AppNumber=None, FileName=None):
		self.FilingDate = None
		self.zf = None
		self.files = []
		self.AppNumber = None
		self.TH = None
		self.AD = None
		self.IssueDate = None
		self.Efiles = []
		
		if AppNumber != None:
			self.Retrieve(AppNumber)
		
		if FileName != None:
		  self.Open(FileName)
	
	#Retrieves file from Google
	# Takes Application number as parameter: 12/102391
	def Retrieve(self, AppNumber):
		
		Number = ''.join(AppNumber.split('/'))
		if len(Number) != 8:
			raise ValueError("Application Number should have 8 numbers")
		URL = "http://storage.googleapis.com/uspto-pair/applications/"+str(Number) +".zip"
		u = urllib2.urlopen(URL)
		workingdir = expanduser("~") + "/ImageFileWrappers/"
		if not os.path.exists(workingdir):
		    os.makedirs(workingdir)
		filename = workingdir + Number + ".zip"
		with open(filename, 'wb') as f:
			shutil.copyfileobj(u, f)
		u.close()
		f.close()
		self.Open(filename)
	
	# Open existing file wrapper .zip file	
	def Open(self, filename):
		self.zf = zipfile.ZipFile(filename, 'r')
		self.files = self.zf.namelist()
		self.AppNumber = self.files[0][0:8] 
		
	#Checks for presence of Notice of Allowance
	def isAllowed(self):
		if self.zf == None:
			raise Exception("ImageFileWrapper not itialized, no .zip file present")
		if self.TH == None:
			self.GetTransactionHistory()
		if re.search('Mail Notice of Allowance', self.TH) != None:
			return True
		else:
			return False

	#Returns Filing Date
	def getFilingDate(self):
		if self.FilingDate != None:
			return self.FilingDate
		if self.zf == None:
			raise Exception("ImageFileWrapper not itialized, no .zip file present")
		if self.AD == None:
			self.GetApplicationData()
		self.FilingDate = self.AD.split('\n')[1].split('\t')[1]
		return self.FilingDate
		
	#Returns Issue Date or '-'	
	def getIssueDate(self):
		if self.IssueDate != None:
			return self.IssueDate
		if self.zf == None:
			raise Exception("ImageFileWrapper not itialized, no .zip file present")
		if self.AD == None:
			self.GetApplicationData()
		self.IssueDate = self.AD.split('\n')[17].split('\t')[1]
		return self.IssueDate

	# Loads the Transaction History file from the .zip file into self.TH
	def GetTransactionHistory(self):
		if self.TH != None:
			return
		THfile = self.AppNumber + '/' + self.AppNumber + '-transaction_history.tsv'
		workingdir = expanduser("~") + "/ImageFileWrappers/"
		filename = self.zf.extract(THfile, workingdir)
		self.Efiles.append(filename) 
		self.TH = open(filename, 'r').read()
	
	def GetApplicationData(self):
		if self.TH != None:
			return
		ADfile = self.AppNumber + '/' + self.AppNumber + '-application_data.tsv'
		workingdir = expanduser("~") + "/ImageFileWrappers/"
		filename = self.zf.extract(ADfile, workingdir)
		print "Extracted: "+ filename
		self.Efiles.append(filename) 
		self.AD = open(filename, 'r').read()
	
	
	def __del__(self):
		for file in self.Efiles:
			os.unlink(file)