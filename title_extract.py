import os
results = 0
with open("wp_titles.txt", "w") as out:
    for filename in sorted(os.listdir('pages')):
        print "Opening file %s"%filename
        with open("pages/%s"%filename, 'r') as f:
            for line in f:
                records = line.split("),")
                for r in records:
                    try:
                        items = r[1:].split(",")
                        out.write("%s %s %s\n"%(items[0],items[1],items[2]))
                        results += 1
                    except:
                        pass
        print "Current results: %s"%results

print "Done!"