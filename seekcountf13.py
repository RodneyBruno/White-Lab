import liblytics
import csv
import time
from sets import Set

videoNames = {}
with open("Video Names 3.csv", "rU") as f:
    reader = csv.reader(f)
    for row in reader:
        videoNames[row[0]] = row[1] #cannot remember how this line works exactly
        
usernames = Set()
with open("Names for SPOC.csv", "rb") as f:
	reader = csv.reader(f)
	for row in reader:
		usernames.add(row[3])

data={} #first dict with username (key) : second dict (value)
def parseEventText(eventLine):
	line = eventLine.replace("{","")
	line = line.replace("}","")
	units = line.split(",")
	result = {}
	for unit in units:
		pieces = unit.split(":")
		result[pieces[0].replace('"',"")] = pieces[1].replace('"',"")

	return result


for line in liblytics.read_log_file("tracking_700x_UMass__Fall_2013.log.gz"): #Reads line in log file
	if (line["event_type"] == "seek_video"):  # Grabs only seek_videos
		username=line["username"]
		newtimes = parseEventText(line["event"])["new_time"] 
		#first loop creates first dict
		if username != "": 
			videoName = parseEventText(line["event"])["id"]
			
			if username not in data:
				data[username] = {}
			usersDict = data[username]
			#creates third dict with playCount and Times (keys) and their values
			if videoName not in usersDict: #second loop creates third dict
				videoDict = {}
				videoDict["New Times"] = []
				videoDict["Seek Video Count"] = 1
				usersDict[videoName] = videoDict
			videoDict = usersDict[videoName]
			videoDict["New Times"].append(newtimes)
			videoDict["Seek Video Count"] = len(videoDict["New Times"])
			usersDict[videoName] = videoDict
			data[username] = usersDict
			

# Prints to CSV
f = open("Total Seek Videos f13.csv", "w") #This is where you could name the CSV
f.write("username,")
for cleanName in sorted(videoNames):
	f.write(cleanName)
	f.write(",")
f.write(" \n")
##for username in sorted(data):
	##if username in usernames:
for username in sorted(usernames):
	if username in data:
		f.write(username)
		f.write(",")
		for cleanName in sorted(videoNames):
			if videoNames[cleanName] in data[username]:
				f.write(str(data[username][videoNames[cleanName]]["Seek Video Count"]))
				f.write(",")	
			else:
				f.write("0,")
		f.write(" \n")
	
f.close()