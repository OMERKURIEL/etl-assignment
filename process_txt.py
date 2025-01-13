import json

def calc_gc_content(sequence):
    length = len(sequence)
    count_c = 0
    count_g = 0
    for char in sequence:
        if char == 'C':
            count_c += 1
        if char == 'G':
            count_g += 1
    return round((100 * (count_c + count_g)) / length, 2)

def compute_codon_frequency(sequence):
    codon_freq = {}
    for i in range(0, len(sequence), 3):
        if sequence[i:i+3] in codon_freq:
            codon_freq[sequence[i:i + 3]] += 1
        else:
            codon_freq[sequence[i:i + 3]] = 1
    return codon_freq

def compute_most_frequent_codon(sequences):
    total_codon_count = {}
    for sequence in sequences:
        # Use compute_codon_frequency to calculate frequency per sequence
        codon_freq = compute_codon_frequency(sequence)
        for codon, count in codon_freq.items():
            if codon in total_codon_count:
                total_codon_count[codon] += count
            else:
                total_codon_count[codon] = count
    most_frequent_codon = max(total_codon_count, key=total_codon_count.get)
    return most_frequent_codon

def compute_longest_common_subsequence(sequences):
    if not sequences:
        return {"value": "", "sequences": [], "length": 0}

    # split the sequences into codons:
    codon_sequences = [
        [sequence[i:i+3] for i in range(0, len(sequence) - len(sequence) % 3, 3)]
        for sequence in sequences
    ]

    lcs = codon_sequences[0]
    for codon in codon_sequences[1:]:
        break

    length = len(lcs)



def process_txt_files(txt_file_path):
    """
    Process the .txt file in the context_path.
    """
    print(f"Processing TXT file: {txt_file_path}")
    with open(txt_file_path, 'r') as file:
        sequences = [line.strip() for line in file if line.strip()] # remove trailing and leading blanks

    print(f"Processing {len(sequences)} sequences from TXT file: {txt_file_path}")

    # initialize the returned variables
    sequence_results = []
    aggregated_codon_frequency = {}
    lcs_result = sequences[0] if sequences else ""

    # traverse through all sequences in the file and compute the per-sequence checks
    for idx, sequence in enumerate(sequences, start=1):
        # compute gc content and codons frequency
        gc_content = calc_gc_content(sequence)
        codons_frequency = compute_most_frequent_codon(sequence)
        # append the result to the list
        sequence_results.append({"gc_content": gc_content,
                                 "codons": codons_frequency})
    # compute most common codon and lcs
    most_common_codon = compute_most_frequent_codon(sequences)
    lcs_result = compute_most_frequent_codon(sequences)

    return {
        "sequences": sequence_results,
        "most_common_codon": most_common_codon,
        "lcs": {
            lcs_result
        }
    }





















