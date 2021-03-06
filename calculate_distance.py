import math
import os


def CA_atoms(clean_pdb):
    with open(clean_pdb) as fin:
        lines = fin.readlines()

    CA_lines = []
    for line in lines:
        if 'CA' in line[12:16]:
            CA_lines.append(line)
        else:
            pass

    prot_CA = clean_pdb[:-4] + '_CA.pdb'
    with open(prot_CA, 'w') as fout:
        for i in range(0, len(CA_lines)):
            fout.write(CA_lines[i])

    fin.close()
    fout.close()
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

    clean_Stride = out_SS[:-3] + '_clean.ss'
    fout = open(clean_Stride, 'w')

    for line in lines:
        if line[0:3] == 'ASG':
            fout.write(line)
        else:
            pass

    fin.close()
    fout.close()
    return clean_Stride


def loop_region(clean_ss):
    with open(clean_ss) as fin1:
        lines = fin1.readlines()

    SS = ['E', 'H', 'G', 'e', 'h', 'g']
    non_SS = ['C', 'T', 'B', 'c', 't', 'b']
    start_res = []
    for i in range(0, (len(lines) - 1)):
        j = i + 1
        if lines[i][24]  in SS:
            if lines[j][24]  in non_SS:
                if int(lines[j][11:15]) < len(lines):
                    start_res.append(int(lines[i][11:15]))
                else:
                    pass
            else:
                pass
        else:
            pass

    end_res = []
    for i in range(1, len(lines)):
        j = i - 1
        if lines[j][24]  in non_SS:
            if lines[i][24]  in SS:
                if int(lines[j][11:15]) > 1:
                    end_res.append(int(lines[i][11:15]))
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

    fin1.close()
    return start_res, end_res


def dist_2pts(x1, y1, z1, x2, y2, z2):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2))
    return '%8.3f' % (dist)


def distance(prot_CA, start_res, end_res, clean_pdb):
    with open(prot_CA) as fin2:
        lines = fin2.readlines()

    start_line = []
    end_line = []
    for line in lines:
        for i in range(0, len(start_res)):
            if int(line[22:26]) == start_res[i]:
                start_line.append(line)
            else:
                pass
        for i in range(0,len(end_res)):
            if int(line[22:26]) == end_res[i]:
                end_line.append(line)
            else:
                pass


    loop_length = []
    loop_dist = []
    for i in range(0, len(start_line)):
        loop_length.append((int(end_line[i][22:26]) - int(start_line[i][22:26])) - 1)
        d = dist_2pts(float(start_line[i][30:38]), float(start_line[i][38:46]), float(start_line[i][46:54]),
                      float(end_line[i][30:38]), float(end_line[i][38:46]), float(end_line[i][46:54]))
        loop_dist.append(float(d))

    loops = clean_pdb[:-4] + '_loop_dist.txt'
    with open(loops, 'w') as fout:
        for i in range(0, len(loop_length)):
            tmp = "%4d" % (loop_length[i]) + "%8.3f" % (loop_dist[i]) + '\n'
            fout.write(tmp)

    fout.close()
    fin2.close()
    return loops


def checkDist(loops, clean_pdb):
    with open(loops) as fin:
        lines = fin.readlines()

    check_file = clean_pdb[:-4] + '_loop_check.txt'
    with open(check_file, 'w') as fout:
        for line in lines:
            t = line.split()
            ideal_dist = float(t[0]) * 3.8
            if float(ideal_dist) >= float(t[-1]):
                temp = "%4d" % int(t[0]) + "%8.3f" % float(t[-1]) + "%6s" % ('OK') + "\n"
                fout.write(temp)
            else:
                temp = "%4d" % int(t[0]) + "%8.3f" % float(t[-1]) + "%6s" % ('ERROR') + "\n"
                fout.write(temp)

    fin.close()
    fout.close()
    return check_file
