from redis import Redis
r = Redis()

results = {}


with open("alma5.txt", "r") as f:
    records = f.readlines()
    for record in records:
        rec,id = record.split(" ")
        if r.hexists("loc",id):
            wiki = r.hget("loc", id)
            title = r.hget("titles", wiki).strip().replace("'","").replace("_"," ")
            if rec in results.keys():
                results[rec]["LOC"].append(title)
            else:
                results[rec] = {"LOC": [title]}
            #print "Match! ALMA: %s LoC: %s Wiki: %s Title: %s"%(rec,id.strip(),wiki,title)

with open("alma-viaf5.txt", "r") as f:
    records = f.readlines()
    for record in records:
        rec, id = record.split(" ")
        if r.hexists("viaf2", id):
            wiki = r.hget("viaf2", id)
            try:
                title = r.hget("titles", wiki).strip().replace("'", "").replace("_", " ")
            except AttributeError:
                title = "Unknown"
            if rec in results.keys():
                if "VIAF" in results[rec].keys():
                    results[rec]["VIAF"].append(title)
                else:
                    results[rec]["VIAF"] = [title]
            else:
                results[rec] = {"VIAF": [title]}
            #print "Match! ALMA: %s VIAF: %s Wiki: %s Title: %s"%(rec,id.strip(),wiki,title)

from pprint import pprint
pprint results