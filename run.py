import sys

import calculate_distance

prot_CA = calculate_distance.CA_atoms(sys.argv[1])
out_SS = calculate_distance.runStride(sys.argv[1])
clean_ss = calculate_distance.clean_SS(out_SS)
start_res, end_res = calculate_distance.loop_region(clean_ss)
lines = calculate_distance.distance(prot_CA, start_res, end_res, sys.argv[1])
