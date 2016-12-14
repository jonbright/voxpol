#creates networks from datasets containing tweets
#assumes each line in the dataset is a json of a standard tweet object from the API

import json
filelist = ["INSERT LIST OF JSON FILES HERE"]

print "Analysing the following files..."
for filename in filelist:
    print filename

print "Processing tweets"

users = {}
user_edges = {}

for filename in filelist:

    print filename
    infile = open(filename, "r")
    
    for i, line in enumerate(infile):

        try:
            obj = json.loads(line.strip())
        except ValueError:
            #corrupt json
            print "Corrupt JSON"
            continue
        
        if not "user" in obj:#could be a deletion message
            continue

		if not obj["user"]['screen_name'] in user_edges:
			user_edges[obj["user"]['screen_name']] = {}

        #now add each relation in the tweet to each user
        for mentioned in obj["entities"]["user_mentions"]:
		
			if not mentioned["screen_name"] in user_edges[obj["user"]['screen_name']]:
				user_edges[obj["user"]['screen_name']][mentioned["screen_name"]]=0
			user_edges[obj["user"]['screen_name']][mentioned["screen_name"]]+=1 

        ####
        #User Stats
        #Record basic stats about each tweeter
        #And also which networks they belong to, and how many times they have tweeted to each network
        ####
        
                
        if not obj["user"]["screen_name"] in users:
            users[obj["user"]["screen_name"]] = {}
            users[obj["user"]["screen_name"]]["data"] = {}
            users[obj["user"]["screen_name"]]["data"]["id_str"] = obj["user"]["id_str"]
            users[obj["user"]["screen_name"]]["data"]["followers_count"] = obj["user"]["followers_count"]
            users[obj["user"]["screen_name"]]["data"]["statuses_count"] = obj["user"]["statuses_count"]
			users[obj["user"]["screen_name"]]["data"]["observed_tweets"]=0
		users[obj["user"]["screen_name"]]["data"]["observed_tweets"]+=1
        
                        
    #loop end
    infile.close()


print count, "tweets processed"
print "Outputting user files"

output = open("VOXPOL Twitter Network User Level Dataset.csv", "w")

output.write("user_id")
output.write(";")
output.write("followers")
output.write(";")
output.write("all time tweets")
output.write(";")
output.write("observed tweets")
output.write("\n")

for user in users:
           
	output.write(user)
	output.write(";")
	output.write(str(users[user]["data"]["followers_count"]))
	output.write(";")
	output.write(str(users[user]["data"]["statuses_count"]))
	output.write(";")
	output.write(str(users[user]["data"]["observed_tweets"]))
	output.write("\n")

output.close()

#edges 

output = open("VOXPOL Twitter Network User-Edges Dataset.csv", "w")

output.write("Source")
output.write(";")
output.write("Target")
output.write(";")
output.write("Weight")
output.write("\n")

for source in user_edges:
	for target in user_edges[source]:
           
		output.write(source)
		output.write(";")
		output.write(target)
		output.write(";")
		output.write(str(user_edges[source][target]))
		output.write("\n")

output.close()

    

