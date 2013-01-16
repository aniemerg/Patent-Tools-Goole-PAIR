# Test script for ImageFileWrapper
# Retrieves some data

from ImageFileWrapper import ImageFileWrapper

def TryIFW():
	number = 11000001
	results = []
	for x in range (1, 3):
		App = number + x
		AppNumber = str(App)
		try:
		  TheApp = ImageFileWrapper.ImageFileWrapper(AppNumber=AppNumber)
		except:
			continue
		AppResult = (AppNumber, TheApp.getFilingDate(), TheApp.getIssueDate())
		results.append(AppResult)
		print "Application Number: %s was filed on %s and issued on %s" % AppResult
	issued = 0
	for x in results:
		if x[2] != '-':
			issued += 1
	total = float(len(results))
	percentage = (issued/total)*100
	print "The percentage of Applications that issued is:%f" % percentage
	
	
	
if __name__=="__main__":
	TryIFW()