import sys
import os  # operating system interface
import numpy as np
import argparse  # command line argument parser
import smash_basic_scripts as sb
from multiprocessing import Pool

parser = argparse.ArgumentParser()
# options and arguments
parser.add_argument("output_file", type=str)
parser.add_argument("pdg_list", type=str)
parser.add_argument("config_file", help="config file")
parser.add_argument("files_to_analyze", nargs='+',
                    help="binary file(s) containing collision history")
args = parser.parse_args()
pdg_list = np.array([int(sb.name_to_pdg(x, args.config_file)) for x in args.pdg_list.split(',')])
total_pdgs = pdg_list.shape[0]
max_tcounter = 500  # max number of blocks per event
time    = np.zeros(max_tcounter)
mul     = np.zeros((max_tcounter, total_pdgs))
mul_sqr = np.zeros((max_tcounter, total_pdgs))
event_num_total = 0
tcounter = 0

for file_to_analyze in args.files_to_analyze:
    print(file_to_analyze)
    event_num_this_file = 0
    with sb.BinaryReader(file_to_analyze) as reader:
        smash_version = reader.smash_version
        #format_version = reader.format_version
        for block in reader:
            if (block['type'] == b'f'):  # end of event
                event_num_total += 1
                event_num_this_file += 1
                blocks_per_event = tcounter
                tcounter = 0
                print(event_num_total)
                # if (event_num_this_file > 49): break
            if (block['type'] == b'i'):  # interaction
                print('Error: there should be no interactions in this file!')
                sys.exit(1)
            if (block['type'] == b'p'):  # particles
                if (event_num_total == 0):
                    time[tcounter] = sb.get_block_time(block)
                E = block['part']['p'][:,0]
                pz = block['part']['p'][:,3]
                y = 0.5*np.log((E+pz)/(E-pz))
                ycut = (np.abs(y) < 1.0)
                pdg = block['part']['pdgid']
                for i in np.arange(total_pdgs):
                    pdgcut = (pdg == pdg_list[i])
                    part_num = np.logical_and(ycut, pdgcut).sum()
                    mul[tcounter, i] += part_num
                    mul_sqr[tcounter, i] += part_num*part_num
                tcounter += 1

mul /= event_num_total  # get average multiplicity
mul_sqr /= event_num_total # get average square of multiplicity
mul_err = np.sqrt((mul_sqr - mul * mul)/(event_num_total - 1))
with open(args.output_file, 'w') as f:
    f.write('# smash and analysis version\n')
    f.write('%s %s\n' % (smash_version, sb.analysis_version_string()))
    f.write('# total number events\n')
    f.write('%d\n' % event_num_total)
    f.write('# pdg codes list\n')
    for i in np.arange(total_pdgs): f.write('%d ' % pdg_list[i])
    f.write('\n')
    f.write('# time moments array [%d]\n' % blocks_per_event)
    for i in np.arange(blocks_per_event): f.write('%.3f ' % time[i])
    f.write('\n')
    for i in np.arange(total_pdgs):
        f.write('# multiplicities and their stat errors of pdg %d versus time\n' % pdg_list[i])
        for j in np.arange(blocks_per_event): f.write('%.5f ' % mul[j, i])
        f.write('\n')
        for j in np.arange(blocks_per_event): f.write('%.5f ' % mul_err[j, i])
        f.write('\n')
