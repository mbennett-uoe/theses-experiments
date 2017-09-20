#import os
results = []
with open("alma2.txt", "w") as out:
    current = {}
    with open("alma2.mrk", 'r') as f:
        for line in f:
            if line.strip() == "":
                out.write("%s %s\n"%(current["id"],current["loc"]))
                current = {}
            else:
                code = line[1:4]
                if code == "001":
                    current["id"] = line[6:].strip()
                if code == "100":
                    loc = line[6:].strip().split("$0")
                    current["loc"] = loc[1].split("/")[-1]