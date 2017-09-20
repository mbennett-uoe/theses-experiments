with open("wp_loc_proc.txt", "w") as out:
    l = 1
    with open("wp_loc.txt") as f:
        for line in f:
            parts = line[1:-1].split(",")
            try:
                out.write("%s %s\n"%(parts[1],parts[3].replace("http://id.loc.gov/authorities/names/","").replace(".html","").replace("'","")))

                #if parts[2] != "0": print line
            except:
                #print "ERR line %s: %s"%(l,line)
                pass
            l += 1