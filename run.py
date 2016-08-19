import sys

import loop_distance

prot_CA = loop_distance.CA_atoms(sys.argv[1])
out_SS = loop_distance.runStride(sys.argv[1])
clean_ss = loop_distance.clean_SS(out_SS)
start_res, end_res = loop_distance.loop_region(clean_ss)
loops = loop_distance.distance(prot_CA, start_res, end_res, sys.argv[1])

