from time import sleep
import requests
with open("alma-viaf3.txt", "w") as out:
    with open("alma3.txt", "r") as f:
        records = f.readlines()
        for record in records:
            rec,id = record.split(" ")
            try:
                resp = requests.get("http://www.viaf.org/viaf/lccn/%s"%id.strip(), allow_redirects=False, timeout=15)
                if resp.status_code == 301:
                    viaf_url = resp.headers["Location"]
                    viaf_id =  viaf_url.split("/")[-1]
                    out.write("%s %s\n"%(rec,viaf_id))
                else:
                    print "NON 301 Response! Record %s" % rec
                    print resp.status_code
            except Exception as e:
                print "ERROR! Record %s" %rec
                print e
            #sleep(5)

