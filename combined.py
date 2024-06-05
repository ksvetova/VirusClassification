
import random

virus_file_path = 'virus-training-sample100K.fa'
host_file_path = 'host-training-sample100K.fa'
output_virus_file_path = 'sampled_virus_data.fa'
output_host_file_path = 'sampled_host_data.fa'
output_combined_file_path = 'combined-sample185.fa'


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


virus_data_pairs = read_fasta(virus_file_path)
host_data_pairs = read_fasta(host_file_path)


available_virus_count = len(virus_data_pairs)
available_host_count = len(host_data_pairs)


print(f"Available virus samples: {available_virus_count}")
print(f"Available host samples: {available_host_count}")


target_size_each = min(available_virus_count, available_host_count)


assert available_virus_count >= target_size_each, "Not enough virus data to sample from"
assert available_host_count >= target_size_each, "Not enough host data to sample from"


sampled_virus_data = random.sample(virus_data_pairs, target_size_each)
sampled_host_data = random.sample(host_data_pairs, target_size_each)


sampled_data_pairs = sampled_virus_data + sampled_host_data
random.shuffle(sampled_data_pairs)  # shuffle data

write_fasta(sampled_virus_data, output_virus_file_path)
write_fasta(sampled_host_data, output_host_file_path)
write_fasta(sampled_data_pairs, output_combined_file_path)


virus_count = len(sampled_virus_data)
host_count = len(sampled_host_data)
print(f"Virus samples: {virus_count}")
print(f"Host samples: {host_count}")

print(f"Sampled virus dataset created at: {output_virus_file_path}")
print(f"Sampled host dataset created at: {output_host_file_path}")
print(f"Combined dataset created at: {output_combined_file_path}")

