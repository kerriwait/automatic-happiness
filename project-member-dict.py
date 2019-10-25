#!/bin/env python

import grp
import pwd 
from collections import defaultdict
import subprocess

thedict = defaultdict(list)
thedict2 = defaultdict(list)
thedict3 = defaultdict(set)

members = grp.getgrnam('M3EarlyAdopters').gr_mem

swgroups = ["kg98", "abaqus-monash", "amber", "pMona0006", "atomprobe", "avizo", "comsol-civil", "cplex", "fsl", "gauss", "gaussianmonash", "gurobi", "hcp500", "hcpdata", "icm", "imagenet", "miakat", "phenix", "rosetta", "stata", "vasp5", "pMona0005", "vasp_nikhilm", "vasp_zliu"]

for member in members:
    res = pwd.getpwnam(member)
    thedict[res.pw_gid].append(member)

for gid in thedict.keys():
    gname = grp.getgrgid(gid).gr_name
    thedict2[gname] = thedict[gid]
    for member in thedict[gid]:
        grps = subprocess.check_output(['id', '-Gn', member]).split()
        for group in grps[1:]:
            if group in swgroups:
                continue
            thedict3[gname].add(group)
    thedict3[gname].remove('M3EarlyAdopters')

for institute in sorted(thedict3.keys()):
    try:
        thedict3[institute] = sorted(thedict3[institute])
    except Exception as e:
        print(e)
    with open('/root/k/kerri/scripts/p{}.sh'.format(institute), 'w') as f:
        if institute == "monashuniversity":
            f.write("#!/bin/bash\n\nfor project in \n# ")
            for idx, val in enumerate(thedict3[institute], start=1):
                f.write("{} ".format(val))
                if idx%100 == 0:
                    f.write(";\n# for project in ")
            f.write("\n  do projectsearch $project {} & \nwhile [ `jobs | grep Running | wc -l` -ge 3 ]; do\n sleep 1\n done;\ndone".format(institute))
        else:        
            f.write("#!/bin/bash\n\nfor project in {};\n  do projectsearch $project {} & \nwhile [ `jobs | grep Running | wc -l` -ge 3 ]; do\n sleep 1\n done;\ndone".format(" ".join(thedict3[institute]), institute))
    with open('/root/k/kerri/scripts/s{}.sh'.format(institute), 'w') as f:
        if institute == "monashuniversity":
            f.write("#!/bin/bash\n\nfor project in \n# ")
            for idx, val in enumerate(thedict3[institute], start=1):
                f.write("{} ".format(val))
                if idx%100 == 0:
                    f.write(";\n# for project in ")
            f.write("\n  do scratchsearch $project {} & \nwhile [ `jobs | grep Running | wc -l` -ge 3 ]; do\n sleep 1\n done;\ndone".format(institute))
        else:
            f.write("#!/bin/bash\n\nfor project in {};\n  do scratchsearch $project {} & \nwhile [ `jobs | grep Running | wc -l` -ge 3 ]; do\n sleep 1\n done;\ndone".format(" ".join(thedict3[institute]), institute))

print(" ,".join(map(lambda x: "\"" + x + "\"", sorted(thedict3.keys()))))
