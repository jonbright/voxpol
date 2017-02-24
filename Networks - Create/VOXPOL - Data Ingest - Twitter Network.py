###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in data from Twitter converts it into network format
#assumes that each line in the input file is a json of a standard tweet object from the API
#this object should contain the name of the poster and the name of any other poster they replied to in that post

#To run, place this script in the same folder as your input data file
#Change the following to the name of your file
filelist = ["INPUT FILE1", "INPUT FILE2"]
#the output will be a file entitled "VOXPOL Twitter Network User-Edges Dataset.csv", a list of edges
#and also "VOXPOL Twitter Network User Level Dataset.csv", a list with basic summary information about each user


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
            #Sometimes data becomes corrupted
            print "Corrupt JSON"
            continue
        
        if not "user" in obj:#could be a deletion message
            continue

        #check user exists
        if not obj["user"]['screen_name'] in user_edges:
            user_edges[obj["user"]['screen_name']] = {}

        #add each relation in the tweet to each user
        for mentioned in obj["entities"]["user_mentions"]:
		
            if not mentioned["screen_name"] in user_edges[obj["user"]['screen_name']]:
                    user_edges[obj["user"]['screen_name']][mentioned["screen_name"]]=0
            user_edges[obj["user"]['screen_name']][mentioned["screen_name"]]+=1 

        #also record basic stats about each tweeter
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

#Output users

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

#Output edges 

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

    

