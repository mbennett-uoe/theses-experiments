with open("VIAFmatches.txt", "w") as out:
    with open("noLOC.txt", "r") as f:
        for line in f:
            alma, marc = line.strip().split(" ", 1)
            data = {}
            for part in marc.split("$"):
               letter = part[0]
               val = part[1:].strip(" ,.")
               data[letter] = val
            print "---%s -- %s---"%(alma,data)
