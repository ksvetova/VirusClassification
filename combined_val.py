import random

virus_file_path = 'virus-training-sample100K.fa'
host_file_path = 'host-training-sample100K.fa'
output_virus_file_path = 'sampled_val_virus_data.fa'
output_host_file_path = 'sampled_val_host_data.fa'

# target total lengths for validation set
target_virus_length = 785691
target_host_length = 750412

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

def sample_sequences_by_length(sequences, target_total_length):
    sampled_sequences = []
    sampled_length = 0
    available_sequences = sequences[:]
    random.shuffle(available_sequences)

    while available_sequences and sampled_length + len(available_sequences[-1][1]) <= target_total_length:
        header, sequence = available_sequences.pop()
        sampled_sequences.append((header, sequence))
        sampled_length += len(sequence)

    # if we didn't reach the target length add one more sequence 
    if available_sequences and sampled_length < target_total_length:
        header, sequence = available_sequences.pop()
        sampled_sequences.append((header, sequence))
        sampled_length += len(sequence)

    # if the total length exceeds the target adjust the last sequence
    if sampled_length > target_total_length:
        excess_length = sampled_length - target_total_length
        header, sequence = sampled_sequences.pop()
        adjusted_sequence = sequence[:-excess_length]
        sampled_sequences.append((header, adjusted_sequence))
        sampled_length = get_total_length(sampled_sequences)

    return sampled_sequences, sampled_length


virus_data_pairs = read_fasta(virus_file_path)
host_data_pairs = read_fasta(host_file_path)

sampled_virus_data, sampled_virus_length = sample_sequences_by_length(virus_data_pairs, target_virus_length)

sampled_host_data, sampled_host_length = sample_sequences_by_length(host_data_pairs, target_host_length)

write_fasta(sampled_virus_data, output_virus_file_path)
write_fasta(sampled_host_data, output_host_file_path)

sampled_virus_average_length = get_total_length(sampled_virus_data) / len(sampled_virus_data) if sampled_virus_data else 0
sampled_host_average_length = get_total_length(sampled_host_data) / len(sampled_host_data) if sampled_host_data else 0
virus_count = len(sampled_virus_data)
host_count = len(sampled_host_data)

print(f"Target virus sequences length: {target_virus_length}")
print(f"Target host sequences length: {target_host_length}")
print(f"Sampled virus sequences length: {sampled_virus_length}")
print(f"Sampled host sequences length: {sampled_host_length}")
print(f"Number of virus samples: {virus_count}")
print(f"Number of host samples: {host_count}")
print(f"Average sampled virus sequence length: {sampled_virus_average_length}")
print(f"Average sampled host sequence length: {sampled_host_average_length}")
print(f"Sampled virus dataset created at: {output_virus_file_path}")
print(f"Sampled host dataset created at: {output_host_file_path}")
