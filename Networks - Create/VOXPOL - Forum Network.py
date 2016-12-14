#takes in scraped forum data
#processes into an edge list which could be read into a gml
#edge list is a convenient format for a very large network

#assumes that each line in the input file is a json of a forum post
#should contain the name of the poster and the name of any other poster they replied to in that post

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

infile = open("FORUM JSOSNS", "r", encoding="utf-8")
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
    


    
