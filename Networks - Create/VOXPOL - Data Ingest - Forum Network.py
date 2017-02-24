###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017

#This file takes in scraped data from a web forum and converts it into network format
#assumes that each line in the input file is a json object of a forum post
#this object should contain the name of the poster and the name of any other poster they replied to in that post

#To run, place this script in the same folder as your input data file
#Change the following to the name of your file
infile_name = "FORUM JSOSNS"
#the output will be a file entitled "VOXPOL - Edge List.csv"


def san(text):
    for c in ["\n", "\r", ","]:
        text = text.replace(c, "")
    return text

def month(datestamp):
    month = datestamp.split("-")[1]
    return month

def day(datestamp):
    day = datestamp.split("-")[2]
    day = day.split("T")[0]
    return day

infile = open(infile_name, "r", encoding="utf-8")
import json, pprint

users = {}

print("Input")
for i, line in enumerate(infile):

    if i % 10000==0:
        print(i)
    
    obj = json.loads(line)

    obj["user"] = san(obj["user"])

    if not obj["user"] in users:
        users[obj["user"]] = {}

    for reply in obj["replied_to"]:
        reply["user"] = san(reply["user"])
  
        if not reply["user"] in users[obj["user"]]:
            users[obj["user"]][reply["user"]] = 0
        users[obj["user"]][reply["user"]] += 1


print("Output")
out = open("VOXPOL - Edge List.csv", "w", encoding="utf-8")
out.write("Source,Target,Weight\n")
for i, source in enumerate(users):
    if i % 10000==0:
        print(i)
    for target in users[source]:

        out.write("\"" + source + "\"")
        out.write(",")
        out.write("\"" + target + "\"")
        out.write(",")
        out.write(str(users[source][target]))
        out.write("\n")

out.close()
    


    
