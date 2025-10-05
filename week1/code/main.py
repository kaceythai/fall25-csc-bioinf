import argparse
# import os # Removed
# import sys # Removed
from dbg import DBG
from utils import read_data, os_path_join # Import the new function

# sys.setrecursionlimit(1000000) # This is not needed in Codon

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', help="path of the data")
    args = parser.parse_args(argv)

    # Use the new compatible function
    short1, short2, long1 = read_data(os_path_join('./', args.data_path))

    dbg = DBG(31, [short1, short2, long1])
    contigs = dbg.get_contigs()

    # Use the new compatible function
    with open(os_path_join('./', args.data_path, 'contig.fasta'), 'w') as f:
        i = 0
        for contig in contigs:
            if len(contig) > 500:
                i += 1
                # Update to a modern f-string
                f.write(f'>contig_{i}\n')
                f.write(contig)
                f.write('\n')

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
