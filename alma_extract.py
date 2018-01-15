#import os
results = []
with open("alma3.txt", "w") as out:
    current = {}
    with open("alma3.mrk", 'r') as f:
        for line in f:
            if line.strip() == ""  and current != {}:
                out.write("%s %s\n"%(current["id"],current["loc"]))
                current = {}
            else:
                code = line[1:4]
                if code == "001":
                    current["id"] = line[6:].strip()
                if code == "100":
                    loc = line[6:].strip().split("$0")
                    if len(loc) == 1:
                        # no LoC ident
                        current = {}
                    else:
                        current["loc"] = loc[1].split("/")[-1]