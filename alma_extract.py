#import os
results = []
with open("alma3.txt", "w") as out, open("noLOC.txt", "w") as out2:
    current = {}
    with open("alma3.mrk", 'r') as f:
        for line in f:
            if line.strip() == "": #  and current != {}:
                if current["loc"] != None:
                    out.write("%s %s\n"%(current["id"],current["loc"]))
                else:
                    out2.write("%s %s\n" % (current["id"], current["l100"]))
                current = {}
            else:
                code = line[1:4]
                if code == "001":
                    current["id"] = line[6:].strip()
                if code == "100":
                    loc = line[6:].strip().split("$0")
                    if len(loc) == 1:
                        # no LoC ident
                        current["l100"] = "$".join(loc[0].split("$")[1:])
                        #line = loc[0].split("$")[1:]
                        #data = {}
                        #for part in line:
                        #    letter = part[0]
                        #    val = part [1:]
                        #    data[letter] = val
                        #current["data"] = data
                        #current["auth"] = "--".join(loc[0].split("$")[1:])
                        current["loc"] = None
                    else:
                        current["loc"] = loc[1].split("/")[-1]