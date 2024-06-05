import random

# Define the file paths
virus_file_path = 'virus-training-sample100K.fa'
host_file_path = 'host-training-sample100K.fa'
output_virus_train_file_path = 'sampled_virus_train_data.fa'
output_virus_val_file_path = 'sampled_virus_val_data.fa'
output_virus_test_file_path = 'sampled_virus_test_data.fa'
output_host_train_file_path = 'sampled_host_train_data.fa'
output_host_val_file_path = 'sampled_host_val_data.fa'
output_host_test_file_path = 'sampled_host_test_data.fa'

# Function to read the fasta file and extract the sequences
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

    # If we didn't reach the target length, add one more sequence to ensure we are close
    if available_sequences and sampled_length < target_total_length:
        header, sequence = available_sequences.pop()
        sampled_sequences.append((header, sequence))
        sampled_length += len(sequence)

    return sampled_sequences, sampled_length

def split_sequences(sequences, total_length, proportions):
    train_prop, val_prop, test_prop = proportions
    train_length = int(total_length * train_prop)
    val_length = int(total_length * val_prop)
    test_length = int(total_length * test_prop)

    random.shuffle(sequences)
    
    train_sequences = []
    train_current_length = 0
    val_sequences = []
    val_current_length = 0
    test_sequences = []
    test_current_length = 0

    for header, sequence in sequences:
        if train_current_length < train_length:
            train_sequences.append((header, sequence))
            train_current_length += len(sequence)
        elif val_current_length < val_length:
            val_sequences.append((header, sequence))
            val_current_length += len(sequence)
        else:
            test_sequences.append((header, sequence))
            test_current_length += len(sequence)

    return train_sequences, val_sequences, test_sequences

# Read the virus and host data
virus_data_pairs = read_fasta(virus_file_path)
host_data_pairs = read_fasta(host_file_path)

# Calculate the total length of all virus sequences
total_virus_length = get_total_length(virus_data_pairs)

# Sample host sequences to match the total length of virus sequences
sampled_host_data, sampled_host_length = sample_sequences_by_length(host_data_pairs, total_virus_length)

# Combine virus and sampled host sequences
combined_data = virus_data_pairs + sampled_host_data
total_combined_length = total_virus_length + sampled_host_length

# Define the proportions for train, validation, and test sets
proportions = (0.64, 0.16, 0.20)  # 80/20 split first for train/val, then 80/20 split of train for train/val

# Split the combined data into training, validation, and test sets
train_val_data, _, test_data = split_sequences(combined_data, total_combined_length, (0.8, 0, 0.2))
train_data, val_data, _ = split_sequences(train_val_data, get_total_length(train_val_data), (0.8, 0.2, 0))

# Separate the virus and host data from the split sets
virus_train_data = [item for item in train_data if item in virus_data_pairs]
virus_val_data = [item for item in val_data if item in virus_data_pairs]
virus_test_data = [item for item in test_data if item in virus_data_pairs]
host_train_data = [item for item in train_data if item in sampled_host_data]
host_val_data = [item for item in val_data if item in sampled_host_data]
host_test_data = [item for item in test_data if item in sampled_host_data]

# Write the split data to the output files
write_fasta(virus_train_data, output_virus_train_file_path)
write_fasta(virus_val_data, output_virus_val_file_path)
write_fasta(virus_test_data, output_virus_test_file_path)
write_fasta(host_train_data, output_host_train_file_path)
write_fasta(host_val_data, output_host_val_file_path)
write_fasta(host_test_data, output_host_test_file_path)

# Print the total lengths, counts, and averages of the split virus and host sequences
def print_summary(name, data):
    total_length = get_total_length(data)
    average_length = total_length / len(data) if data else 0
    count = len(data)
    print(f"{name} - Total length: {total_length}, Average length: {average_length}, Number of samples: {count}")

print_summary("Virus Train", virus_train_data)
print_summary("Virus Validation", virus_val_data)
print_summary("Virus Test", virus_test_data)
print_summary("Host Train", host_train_data)
print_summary("Host Validation", host_val_data)
print_summary("Host Test", host_test_data)
