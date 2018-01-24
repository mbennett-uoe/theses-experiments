import requests
import xml.etree.ElementTree as ET

# xml namespaces
ns = {'srw': 'http://www.loc.gov/zing/srw/', 'v': 'http://viaf.org/viaf/terms#'}

def viafSearch(name, dates = None, qualifier = None, precision = "all", matching = "all"):
    # precision types:
    # all: use all available data
    # date: match on name and date
    # qual: match on name and qualifier
    # name: match on name only

    # matching types:
    # exact - exact string including punctuation
    # all - match all search terms

    baseurl = "http://viaf.org/viaf/search?httpAccept=application/xml&recordSchema=http://viaf.org/BriefVIAFCluster&query=local.mainHeadingEl"

    if matching == "exact":
        baseurl += "+exact"
    else:
        baseurl += "+all"

    basename = "\"%s"%name

    if precision == "date":
        if dates:
            basename += " %s"%dates
    elif precision == "qual":
        if qualifier:
            basename += " %s"%qualifier
    elif precision == "name":
        pass
    else:
        if qualifier: basename += " %s"%qualifier
        if dates: basename += " %s"%dates

    basename += "\""

    url = "%s+%s"%(baseurl,basename)
    #print url
    response = requests.get(url)

    return response

def viafProcess(results):
    root = ET.fromstring(results)
    count = root.find("./srw:numberOfRecords", ns).text
    personalrecords = root.findall("./srw:records/srw:record/srw:recordData/v:VIAFCluster/[v:nameType='Personal']",ns)
    #withLOC = personalrecords.findall("./v:mainHeadings/v:data/v:sources/[v:s='LC']/v:sid", ns)
    #matches = []

    if count == "0":
        return 0, None
    else:
        result = {}
        pcount = len(personalrecords)
        result["personal"] = pcount
        if pcount > 1:
            result["id"] = ",".join([rec.find("./v:viafID", ns).text for rec in personalrecords])
            result["loc"] = ",".join([rec.find("./v:mainHeadings/v:data/v:sources/[v:s='LC']/v:sid", ns).text for rec in personalrecords if rec.find("./v:mainHeadings/v:data/v:sources/[v:s='LC']/v:sid", ns) is not None])
        elif pcount == 0:
            result["error"] = "nopersonal"
        elif pcount == 1:
            rec = personalrecords[0]
            result["id"] = rec.find("./v:viafID", ns).text
            if rec.find("./v:mainHeadings/v:data/v:sources/[v:s='LC']/v:sid", ns) is not None:
                result["loc"] = rec.find("./v:mainHeadings/v:data/v:sources/[v:s='LC']/v:sid", ns).text
            else:
                result["loc"] = ""
        else:
            # uh-oh! abort! abort!
            exit("IF THIS HAPPENS, SOMETHING IS HORRIBLY WRONG")
        #matches.append(result)
        return count, result

    #return count, matches

def doSearch(alma, data):

    # search preference order
    precision = ["all", "qual", "date"]#, "name"] # only search if there's more than just a name
    match = ["exact", "all"]

    record_data, available_precision = {}, []
    if "a" in data.keys(): # name
        record_data["name"] = data["a"]
        available_precision.append("name")
    if "d" in data.keys() and data["d"][:6] != "active": # usable DoB/DoD
        record_data["date"] = data["d"]
        available_precision.append("date")
    if "q" in data.keys(): # longer form of name
        record_data["qual"] = data["q"]
        available_precision.append("qual")
    if len(available_precision) > 2: # name, date and qualifier!
        available_precision.append("all")

    # start cycling through searches until we get a result
    if len(available_precision) >= 2:
        print "Alma ID: ", alma
        print "Data: ", data

    for p in precision:
        if p in available_precision:
            print "Trying precision: ", p

            for m in match:
                print "Trying match: ", m

                res = viafSearch(name = record_data.get("name"),
                                 dates = record_data.get("date"),
                                 qualifier= record_data.get("qual"),
                                 precision = p,
                                 matching = m)
                #print res.content
                count, records = viafProcess(res.content)

                if count == 0:
                    #return None
                    pass
                    #print "No matches found"
                else:
                    print count, " matches found - ", records["personal"], " Personal records"
                    return records

        else:
            pass
            #print "Precision unavailable: ", p

#doSearch(9924012224502466, {'a': 'Mackay, W. P', 'q': '(William Paton)', 'e': 'author', 'd': '1839-1885'})

p = open("VIAFmatches.txt", "r")
alist = []
for line in p:
    alma = line.split(",")[0]
    alist.append(alma)

#print alist
#raw_input()

with open("VIAFmatches3.txt", "w") as out:
    with open("noLOC.txt", "r") as f:
        a = 0
        for line in f:
            a = a + 1
            if a % 100 == 0: print "########## %s ###########"%a
            alma, marc = line.strip().split(" ", 1)
            data = {}
            for part in marc.split("$"):
               letter = part[0]
               val = part[1:].strip(" ,.")
               data[letter] = val
            if alma not in alist: # dont bother looking for things we already matched!
                result = doSearch(alma, data)
                if result:
                    line = '%s,"%s","%s"'%(alma,result["id"],result["loc"])
                    out.write("%s\n"%line)
           # response = requests.get()
           # print "---%s -- %s---"%(alma,data)
