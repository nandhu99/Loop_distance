import glob
import os

pdb_files = glob.glob("/home/nandhu/PycharmProjects/Loop_distance/pdbs/*[0-9].pdb")
print len(pdb_files)

for i in range(0, len(pdb_files)):
    print pdb_files[i]
    cmd = 'python run.py ' + pdb_files[i]
    os.system(cmd)
