import argparse
import smash_basic_scripts as sb

parser = argparse.ArgumentParser()
parser.add_argument("files_to_analyze", nargs='+',
                    help="binary file(s) containing collision history")
args = parser.parse_args()

def analyze_file(path):
    print(path)
    event_num = 0
    intcounter = 0
    with sb.BinaryReader(path) as reader:
        smash_version = reader.smash_version

        for block in reader:
            if (block['type'] == b'f'):  # end of event
                event_num += 1
                print("event", event_num, intcounter, "interactions total in this event")
                intcounter = 0
            if (block['type'] == b'i'):  # interaction
                intcounter += 1

for file_to_analyze in args.files_to_analyze:
    analyze_file(file_to_analyze)
