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
	if (line["event_type"] == "play_video"):  # Grabs only play_videos
		username=line["username"]
		t = time.strptime(line['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f") 
		times = time.mktime(t)
		#first loop creates first dict
		if username != "": 
			videoName = parseEventText(line["event"])["id"]
			if videoName == "i4x-MITx-7_00x_UMass-video-DNA_Sequencing_Implementation": #Input video id 
				if username not in data:
					data[username] = {}
				usersDict = data[username]
			#creates third dict with playCount and Times (keys) and their values
				if videoName not in usersDict: #second loop creates third dict
					videoDict = {}
					videoDict["Times"] = []
					videoDict["Playcount"] = 1
					usersDict[videoName] = videoDict
				videoDict = usersDict[videoName]
				videoDict["Times"].append(times)
				videoDict["Playcount"] = len(videoDict["Times"])
				usersDict[videoName] = videoDict
				data[username] = usersDict
			
#calculate list of differences
monsterList25p3F13 = [] #list is made of the output
for username in sorted(usernames):
	if username in data:
		usersDict = data[username]
		for cleanName in sorted(videoNames):
			if videoNames[cleanName] in data[username]:
				videoDict = usersDict[videoNames[cleanName]]
				filtered_playtime_list = []
				playtime_list = videoDict["Times"]
				LPT = 0  # start at 0 so you automatically include the first play_video event
				for playtime in sorted(playtime_list):
					T2 = playtime
					diff = T2 - LPT
					#set time window by changing the number below
					if diff > 1800:
						filtered_playtime_list.append(T2)
						monsterList25p3F13.append(T2)
						LPT=T2
						videoDict["Filtered_play_list"]=filtered_playtime_list
						videoDict["Filtered Plays"]= len(videoDict["Filtered_play_list"])

f = open("Playtime 25.3 DNA REC 2F13.csv", "w") #Output is made to CSV
for x in monsterList25p3F13:
	f.write(str(x))
	f.write("\n")
	
f.close()

