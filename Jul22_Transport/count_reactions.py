import sys
import os
from collections import Counter
from multiprocessing import Pool
#import cPickle as pickle
import numpy as np
import argparse
import yaml
import smash_basic_scripts as sb


def sorted_array_size1or2_equal(a1, a2):
    if a1.size == 1:
        return a2.size == 1 and a1[0] == a2[0]
    if a1.size == 2:
        return a2.size == 2 and a1[0] == a2[0] and a1[1] == a2[1]
    return False

sep = ',:|'
def translate_reaction_string(s):
    """Replace PDG codes with generic particle names."""
    new = []
    last_start = 0

    def get_name(last_start, i):
        pdg_code = int(s[last_start:i])
        name = sb.pdg_to_name(pdg_code)
        return name

    for i in range(len(s)):
        if s[i] not in sep:
            continue
        else:
            new.append(get_name(last_start, i))
            new.append(s[i])
            last_start = i + 1
    new.append(get_name(last_start, len(s)))
    return ''.join(new)

def dedup(l):
    """Deduplicate a list."""
    seen = set()
    seen_add = seen.add  # avoid function lookup in loop
    return [x for x in l if not (x in seen or seen_add(x))]

parser = argparse.ArgumentParser()
# options and arguments
parser.add_argument("--production", type=str, nargs=1, default='',
                    help="count via which channels the given particles are produced")
parser.add_argument("rate_output", type=str,
                    help="file where the reaction rates will be written")
parser.add_argument("production_output", type=str,
                    help="file where the number of produced particles will be written")
parser.add_argument("reactions_string", type=str,
                    help="the reactions that should be analyzed")
parser.add_argument("tstart", type=float,
                    help="ignore everything before this time")
parser.add_argument("config_file", help="config file")
parser.add_argument("files_to_analyze", nargs='+',
                    help="binary file(s) containing collision history")
args = parser.parse_args()

# Read some parameter from config
#configpath = os.path.join(
#    os.path.dirname(args.files_to_analyze[0]), 'config.yaml')
#with open(configpath, 'r') as f:
#    config = yaml.load(f)
end_time = 100.0  #config['General']['End_Time']
N_testparticles = 1 #config['General']['Testparticles']

# Transform reactions string into array form
reactions_list = []
reactions_str = args.reactions_string.split('|')
for reaction_str in reactions_str:
    in_str, out_str = reaction_str.split(':')
    if 'x' in in_str:
        in_str = in_str.split('x')[1]
    reac_in = np.sort(np.array(in_str.split(',')))
    reac_out = np.sort(np.array(out_str.split(',')))
    reactions_list.append([reac_in, reac_out])
    reactions_list.append([reac_out, reac_in])
reactions_number = len(reactions_list)

production_particles = args.production[0].split(',') if args.production else []
def analyze_file(path):
    print(path)
    time_list = [[] for _ in range(reactions_number)]
    other_time_list = []

    # Determine particles for which the production reactions should be counted
    production_counters = [Counter() for _ in range(len(production_particles))]

    intcounter = 0  # any interactions counter
    event_num = 0  # event counter
    produced_particles = Counter()

    # Read input file, add time of given reactions to list: forward and backward
    with sb.BinaryReader(path) as reader:
        smash_version = reader.smash_version
        #format_version = reader.format_version

        for block in reader:
            if (block['type'] == b'f'):  # end of event
                event_num += 1
                #print("event", event_num)
                #if (event_num > 20): break
            if (block['type'] == b'i'):  # interaction
                intcounter += 1
                #  if (intcounter % 10000 == 0): print("interaction ", intcounter)
                time = sb.get_block_time(block)
                if (time < args.tstart):
                    continue
                block_pdgin = np.sort([sb.pdg_to_name(x, args.config_file)
                                      for x in block['incoming']['pdgid']])
                block_pdgout = np.sort([sb.pdg_to_name(x, args.config_file)
                                       for x in block['outgoing']['pdgid']])
                # Only count reactions at midrapidity
                E = block['incoming']['p'][:,0].sum()
                pz = block['incoming']['p'][:,3].sum()
                y = 0.5 * np.log((E+pz)/(E-pz))
                if (np.abs(y) > 1.0):
                    continue
                # fill time histograms
                found_something = False
                for i in range(reactions_number):
                    if (sorted_array_size1or2_equal(reactions_list[i][0], block_pdgin) and
                        sorted_array_size1or2_equal(reactions_list[i][1], block_pdgout)):
                        time_list[i].append(time)
                        #assert not found_something
                        found_something = True
                        #break
                if not found_something and not sb.is_elastic22(block):
                    other_time_list.append(time)
                    # print('***', block_pdgin, '->', block_pdgout)

                # count production reaction
                for i, particle in enumerate(production_particles):
                    if particle not in block_pdgout:
                        continue
                    str_in = ''.join(block_pdgin)
                    str_out = ''.join(block_pdgout)
                    production_counters[i][(str_in, str_out)] += 1

                # count created particles
                produced = set(block_pdgout).difference(set(block_pdgin))
                produced_particles.update(produced)
    return {
        'produced_particles': produced_particles,
        'production_counters': production_counters,
        'time_list': time_list,
        'other_time_list': other_time_list,
        'event_num': event_num,
        'smash_version': smash_version,
    }

def merge_counters(a, b):
    for k, v in iter(b.items()):
        a[k] += v

def merge_time_list(a, b):
    for i in range(len(a)):
        a[i].extend(b[i])

def merge_other_time_list(a, b):
    a.extend(b)

def merge_results(a, b):
    merge_counters(a['produced_particles'], b['produced_particles'])
    for i, j in zip(a['production_counters'], b['production_counters']):
        merge_counters(i, j)
    merge_time_list(a['time_list'], b['time_list'])
    merge_other_time_list(a['other_time_list'], b['other_time_list'])
    a['event_num'] += b['event_num']
    assert a['smash_version'] == b['smash_version']
pool = Pool()
results = pool.map(analyze_file, args.files_to_analyze)
pool.close()
#results = []
#for file_to_analyze in args.files_to_analyze:
#    results.append(analyze_file(file_to_analyze))
assert len(results) >= 1
result = results[0]
for other_result in results[1:]:
    merge_results(result, other_result)
produced_particles = result['produced_particles']
production_counters = result['production_counters']
time_list = result['time_list']
other_time_list = result['other_time_list']
event_num = result['event_num']
smash_version = result['smash_version']

# Normalize counts and print them
def print_most_common(x):
    for key, freq in x:
        if not isinstance(key, str) and len(key) == 2:
            print('(({}, {}), {}) '.format(str(key[0]), str(key[1]), str(freq)))
        else:
            print('({}, {}) '.format(str(key), str(freq)))

for k, v in iter(produced_particles.items()):
    produced_particles[k] = float(v) / event_num
for i, particle in enumerate(production_particles):
    for k, v in iter(production_counters[i].items()):
        production_counters[i][k] = float(v) / event_num
#print('Most commonly produced particles:')
#print_most_common(produced_particles.most_common())
for i, particle in enumerate(production_particles):
    print('Most common production channels for {}:'.format(particle))
    print_most_common(production_counters[i].most_common())

# Prepare time histograms
nbins = 51
binning = np.linspace(args.tstart, end_time, num=nbins)
bin_centers = 0.5 * (binning[0:nbins-1] + binning[1:nbins])  # bin centers

# Write output
with open(args.rate_output, 'w') as f:
    f.write('# smash and analysis version\n')
    f.write('%s %s\n' % (smash_version, sb.analysis_version_string()))
    f.write('# total number events\n')
    f.write('%d\n' % event_num)
    f.write('# number of test particles\n')
    f.write('%d\n' % N_testparticles)
    f.write('# total time\n')
    f.write('%.2f\n' % end_time)
    f.write('# time to start counting reactions\n')
    f.write('%.2f\n' % args.tstart)
    f.write('# list of all reaction analyzed\n')
    f.write('%s\n' % '|'.join(reactions_str))
with open(args.rate_output, 'a') as f:
    for i in range(reactions_number//2):
        f.write('# reaction - %s, time bins, forward and backward\n' % reactions_str[i])
        yf = np.histogram(time_list[2*i], bins=binning)[0]
        yb = np.histogram(time_list[2*i+1], bins=binning)[0]
        np.savetxt(f, bin_centers, fmt='%.3f', newline=' ')
        f.write('\n')
        np.savetxt(f, yf, fmt='%i', newline=' ')
        f.write('\n')
        np.savetxt(f, yb, fmt='%i', newline=' ')
        f.write('\n')
    f.write('# other inelastic reactions\n')
    np.savetxt(f, bin_centers, fmt='%.3f', newline=' ')
    f.write('\n')
    y = np.histogram(other_time_list, bins=binning)[0]
    np.savetxt(f, y, fmt='%i', newline=' ')
    f.write('\n')
#with open(args.production_output, 'w') as f:
#    pickle.dump(produced_particles.most_common(), f)
