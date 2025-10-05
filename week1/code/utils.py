

def os_path_join(*args):
    """A Codon-compatible replacement for os.path.join."""
    return '/'.join(args)

def read_data(path):
    """
    Read data from fasta files.
    This version matches the assignment's target repository.
    """
    data_list = []
    for name in ['short_1.fasta', 'short_2.fasta', 'long.fasta']:
        # Use the new compatible function
        with open(os_path_join(path, name), 'r') as f:
            f.readline() # Skip the header line (e.g., >short_1)
            data_list.append(f.readline().strip()) # Read and store the sequence line
    return data_list[0], data_list[1], data_list[2]


def read_fasta(path, name):
    data = []
    with open(os.path.join(path, name), 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] != '>':
                data.append(line)
    print(name, len(data), len(data[0]))
    # print('Sample:', data[0])
    return data

