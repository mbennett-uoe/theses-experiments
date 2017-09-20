from redis import Redis
r = Redis()
with open("wp_viaf_proc.txt", "r") as f:
    for line in f:
        wiki_id, viaf_url = line.split(" ")
        viaf_url = viaf_url.replace("'","").replace("http://", "").replace("https://","").replace("www.","")
        if viaf_url.startswith("viaf.org/viaf/"):
            viaf_id = viaf_url.split("/")[2]
        elif viaf_url.startswith("viaf.org/"):
            viaf_id = viaf_url.split("/")[1]
        elif viaf_url.startswith("'viaf.org/processed"):
            # reresolve these maybe?
            viaf_id = ""
        else:
            viaf_id = ""

        viaf_id = viaf_id.replace("'","")

        if viaf_id != "":
            res = r.hset("viaf2", viaf_id, wiki_id)
        else:
            print "vid failed: %s"%(viaf_url)
