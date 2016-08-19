import math
import os
import sys


def CA_atoms(clean_pdb):
    with open(clean_pdb) as fin:
        lines = fin.readlines()
    prot_CA = []
    for line in lines:
        if 'CA' in line[12:16]:
            prot_CA.append(line)
        else:
            pass
    fin.close()
    return prot_CA


def runStride(clean_pdb):
    stride = './stride '
    in_pdb = clean_pdb
    out_SS = in_pdb[:-4] + '.ss'
    run_cmd = stride + in_pdb + " > " + out_SS
    os.system(run_cmd)
    return out_SS


def clean_SS(out_SS):
    with open(out_SS) as fin:
        lines = fin.readlines()
    clean_ss = []
    for line in lines:
        if line[0:3] == 'ASG':
            clean_ss.append(line)
        else:
            pass
    fin.close()
    return clean_ss


def loop_region(clean_ss):
    SS = ['E', 'H', 'G', 'e', 'h', 'g']
    non_SS = ['C', 'T', 'B', 'c', 't', 'b']
    start_res = []
    for i in range(0, len(clean_ss)):
        j = i + 1
        if clean_ss[i][24] in SS:
            if clean_ss[j][24] in non_SS:
                if int(clean_ss[j][11:15]) < len(clean_ss):
                    start_res.append(int(clean_ss[i][11:15]))
                else:
                    pass
            else:
                pass
        else:
            pass

    end_res = []
    for i in range(1, len(clean_ss)):
        j = i - 1
        if clean_ss[j][24] in non_SS:
            if clean_ss[i][24] in SS:
                if int(clean_ss[j][11:15]) > 1:
                    end_res.append(int(clean_ss[i][11:15]))
                else:
                    pass
            else:
                pass
        else:
            pass

    if len(end_res) >= len(start_res):
        for i in range(0, (len(start_res) - 1)):
            if start_res[i] > end_res[i]:
                del end_res[i]

    if len(start_res) > len(end_res):
        for i in range(0, len(end_res)):
            if start_res[-1] > end_res[-1]:
                del start_res[-1]

    return start_res, end_res


def dist_2pts(x1, y1, z1, x2, y2, z2):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2))
    return '%8.3f' % (dist)


def distance(prot_CA, start_res, end_res, clean_pdb):
    start_line = []
    end_line = []
    for i in range(0, len(prot_CA)):
        for j in range(0, len(start_res)):
            if int(prot_CA[i][22:26]) == start_res[j]:
                start_line.append(prot_CA[i])
        for k in range(0, len(end_res)):
            if int(prot_CA[i][22:26]) == end_res[k]:
                end_line.append(prot_CA[i])
            else:
                pass

    loop_length = []
    loop_dist = []
    for i in range(0, len(start_line)):
        loop_length.append((int(end_line[i][22:26]) - int(start_line[i][22:26])) - 1)
        d = dist_2pts(float(start_line[i][30:38]), float(start_line[i][38:46]), float(start_line[i][46:54]),
                      float(end_line[i][30:38]), float(end_line[i][38:46]), float(end_line[i][46:54]))
        loop_dist.append(float(d))

    return loop_length, loop_dist


prot_CA = CA_atoms(sys.argv[1])
out_SS = runStride(sys.argv[1])
clean_ss = clean_SS(out_SS)
start_res, end_res = loop_region(clean_ss)
loops = distance(prot_CA, start_res, end_res, sys.argv[1])
print loops