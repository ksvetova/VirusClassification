# works for training

import random

virus_file_path = 'virus-training-sample100K.fa'
host_file_path = 'host-training-sample100K.fa'
output_virus_file_path = 'sampled_virus_data.fa'
output_host_file_path = 'sampled_host_data.fa'

target_virus_count = None  # in case you want specify exact number of virus samples otherwise
# target_virus_count = None  # will be taken the minimum # of both samples available in the dataset

def read_fasta(file_path):
    with open(file_path, 'r') as file:
        sequences = []
        current_header = ''
        current_sequence = ''
        for line in file:
            if line.startswith('>'):
                if current_header and current_sequence:
                    sequences.append((current_header, current_sequence))
                current_header = line.strip()
                current_sequence = ''
            else:
                current_sequence += line.strip()
        if current_header and current_sequence:
            sequences.append((current_header, current_sequence))
    return sequences

def write_fasta(sequences, file_path):
    with open(file_path, 'w') as file:
        for header, sequence in sequences:
            file.write(header + '\n')
            file.write(sequence + '\n')

def get_total_length(sequences):
    return sum(len(sequence) for _, sequence in sequences)

def get_average_length(sequences):
    return get_total_length(sequences) / len(sequences) if sequences else 0

def sample_sequences_by_length(sequences, target_total_length):
    sampled_sequences = []
    sampled_length = 0
    available_sequences = sequences[:]
    random.shuffle(available_sequences)

    while available_sequences and sampled_length + len(available_sequences[-1][1]) <= target_total_length:
        header, sequence = available_sequences.pop()
        sampled_sequences.append((header, sequence))
        sampled_length += len(sequence)

    return sampled_sequences, sampled_length

def sample_sequences_by_count(sequences, target_count):
    return random.sample(sequences, target_count), get_total_length(random.sample(sequences, target_count))

virus_data_pairs = read_fasta(virus_file_path)
host_data_pairs = read_fasta(host_file_path)

# find the total lengths of virus and host data
total_virus_length = get_total_length(virus_data_pairs)
total_host_length = get_total_length(host_data_pairs)

# find the average lengths of virus and host data
average_virus_length = get_average_length(virus_data_pairs)
average_host_length = get_average_length(host_data_pairs)

print(f"Total virus sequences length: {total_virus_length}")
print(f"Total host sequences length: {total_host_length}")
print(f"Average virus sequence length: {average_virus_length}")
print(f"Average host sequence length: {average_host_length}")

if target_virus_count is not None:
    # the exact number of viruses 
    sampled_virus_data, sampled_virus_length = sample_sequences_by_count(virus_data_pairs, target_virus_count)
else:
    # find the target total length for balancing the classes
    target_total_length = min(total_virus_length, total_host_length)
    sampled_virus_data, sampled_virus_length = sample_sequences_by_length(virus_data_pairs, target_total_length)

sampled_host_data, sampled_host_length = sample_sequences_by_length(host_data_pairs, sampled_virus_length)

write_fasta(sampled_virus_data, output_virus_file_path)
write_fasta(sampled_host_data, output_host_file_path)

sampled_virus_average_length = get_average_length(sampled_virus_data)
sampled_host_average_length = get_average_length(sampled_host_data)
virus_count = len(sampled_virus_data)
host_count = len(sampled_host_data)

print(f"Sampled virus sequences length: {sampled_virus_length}")
print(f"Sampled host sequences length: {sampled_host_length}")
print(f"Number of virus samples: {virus_count}")
print(f"Number of host samples: {host_count}")
print(f"Average sampled virus sequence length: {sampled_virus_average_length}")
print(f"Average sampled host sequence length: {sampled_host_average_length}")

print(f"Sampled virus dataset created at: {output_virus_file_path}")
print(f"Sampled host dataset created at: {output_host_file_path}")
