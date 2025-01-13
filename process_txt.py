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
    for i in range(0, len(sequence) - len(sequence) % 3, 3):
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

    # Initialize the LCS as the first sequence
    lcs = sequences[0]
    sequence_indices = [1]  # Assume LCS appears in the first sequence (1-based index)

    for i, sequence in enumerate(sequences[1:], start=2):
        temp_lcs = ""
        for j in range(len(lcs)):
            for k in range(j + 1, len(lcs) + 1):
                sub = lcs[j:k]
                if sub in sequence and len(sub) > len(temp_lcs):
                    temp_lcs = sub
        lcs = temp_lcs
        if lcs:
            sequence_indices.append(i)

    return {"value": lcs, "sequences": sequence_indices, "length": len(lcs)}


def find_lcs_between_two(lcs, sequence):
    """
    Find the longest common subsequence between two sequences.

    :param lcs: The first sequence as a string, the current lcs
    :param sequence: The second sequence as a string, the current sequence checked
    :return: The lcs as a string.
    """
    while lcs:
        if lcs in sequence:
            return lcs  # Found lcs in the sequence
        lcs = lcs[:-1]  # Shorten the lcs by removing the last character

    return ""


def process_txt_files(txt_file_path):
    """
    Process the .txt file in the context_path.
    """
    print(f"Processing TXT file: {txt_file_path}")
    with open(txt_file_path, 'r') as file:
        sequences = [line.strip() for line in file if line.strip()] # remove trailing and leading blanks

    # initialize the returned variable
    sequence_results = []

    # traverse through all sequences in the file and compute the per-sequence checks
    for idx, sequence in enumerate(sequences, start=1):
        # compute gc content and codons frequency
        gc_content = calc_gc_content(sequence)
        codons_frequency = compute_codon_frequency(sequence)
        # append the result to the list
        sequence_results.append({"gc_content": gc_content,
                                 "codons": codons_frequency})
    # compute most common codon and lcs
    most_common_codon = compute_most_frequent_codon(sequences)
    lcs_result = compute_most_frequent_codon(sequences)

    return {
        "sequences": sequence_results,
        "most_common_codon": most_common_codon,
        "lcs":
            lcs_result

    }





















