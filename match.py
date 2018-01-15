from redis import Redis
r = Redis()

with open("alma3.txt", "r") as f:
    records = f.readlines()
    for record in records:
        rec,id = record.split(" ")
        if r.hexists("loc",id):
            wiki = r.hget("loc", id)
            title = r.hget("titles", wiki).strip().replace("'","").replace("_"," ")
            print "Match! ALMA: %s LoC: %s Wiki: %s Title: %s"%(rec,id.strip(),wiki,title)

with open("alma-viaf3.txt", "r") as f:
    records = f.readlines()
    for record in records:
        rec, id = record.split(" ")
        if r.hexists("viaf2", id):
            wiki = r.hget("viaf2", id)
            title = r.hget("titles", wiki).strip().replace("'", "").replace("_", " ")
            print "Match! ALMA: %s VIAF: %s Wiki: %s Title: %s"%(rec,id.strip(),wiki,title)

