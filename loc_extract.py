import os
results = 0
with open("wp_loc.txt", "w") as out:
    for filename in sorted(os.listdir('infiles')):
        print "Opening file %s"%filename
        with open("infiles/%s"%filename, 'r') as f:
            for line in f:
                records = line.split("),")
                for r in records:
                    if r.find("http://id.loc.gov/authorities/names/") > 1:
                        out.write("%s\n"%r)
                        results += 1
        print "Current results: %s"%results

print "Done!"