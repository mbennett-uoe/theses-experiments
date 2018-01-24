with open("alma-viaf-gav.txt", "w") as out_v, open("alma4.txt", "w") as out_l:
    with open("VIAFmatches2.txt", "r") as infile:
        for line in infile:
            alma,ids = line.split(",", 1)
            viaf,loc = ids[1:-1].split('","')
            out_v.write("Alma ID: %s Potential VIAF records: %s\n"%(alma,viaf))
            #for v in viaf.split(","): out_v.write("%s %s\n"%(alma, v))
            if loc.strip('"') != '':
               for l in loc.strip('"').split(","): out_l.write("%s %s\n"%(alma, l))
