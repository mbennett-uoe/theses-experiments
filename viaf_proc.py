with open("wp_viaf_proc.txt", "w") as out:
    l = 1
    with open("wp_viaf.txt") as f:
        for line in f:
            parts = line[1:-1].split(",")
            try:
                if parts[3].startswith("'http://viaf.org/viaf/search"):
                    pass
                elif parts[3] == "'http://viaf.org/'":
                    pass
                else:
                    out.write("%s %s\n"%(parts[1],parts[3]))

                #if parts[2] != "0": print line
            except:
                #print "ERR line %s: %s"%(l,line)
                pass
            l += 1