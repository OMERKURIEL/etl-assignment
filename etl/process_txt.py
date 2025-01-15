from multiprocessing import Pool, cpu_count
from itertools import combinations
import logging


def calc_gc_content(sequence):
    """
    Calculate the GC content of a DNA sequence as a percentage.

    :param sequence: A string representing the DNA sequence.
    :return: GC content percentage, rounded to two decimal places.
    """
    logging.debug("Calculating GC content.")
    length = len(sequence)
    count_c = 0
    count_g = 0
    for char in sequence:
        if char == 'C':
            count_c += 1
        if char == 'G':
            count_g += 1
    gc_content = round((100 * (count_c + count_g)) / length, 2)
    logging.debug("GC content of DNA sequence is %f.", gc_content)
    return gc_content

def compute_codon_frequency(sequence):
    """
    Compute the frequency of codons (triplets of bases) in a DNA sequence.

    :param sequence: A string representing the DNA sequence.
    :return: A dictionary with codons as keys and their frequencies as values.
    """
    logging.debug("Computing codon frequency.")
    codon_freq = {}
    for i in range(0, len(sequence) - len(sequence) % 3, 3):
        if sequence[i:i+3] in codon_freq:
            codon_freq[sequence[i:i + 3]] += 1
        else:
            codon_freq[sequence[i:i + 3]] = 1
    logging.debug(f"Codon frequency: {codon_freq}")
    return codon_freq

def compute_most_frequent_codon(sequences):
    """
    Compute the most frequent codon across multiple DNA sequences.

    :param sequences: A list of strings, each representing a DNA sequence.
    :return: The most frequent codon as a string.
    """
    logging.debug("Computing longest common subsequence (LCS).")
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


def find_lcs_pair(seq1, seq2):
    """Find the longest common subsequence between two sequences."""
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to find the actual subsequence
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            lcs.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs))


def compute_longest_common_subsequence(sequences):
    """
    Find the longest common subsequence among all possible combinations of sequences.
    Returns a dictionary containing the LCS value, list of sequence indices, and length of the lcs.
    """
    if not sequences:
        return {"value": "", "sequences": [], "length": 0}

    max_lcs = ""
    max_indices = []
    max_sequence_count = 0

    # Try all possible combinations of sequences
    for subset_size in range(2, len(sequences) + 1):
        for combo in combinations(range(len(sequences)), subset_size):
            # Find LCS for current combination
            current_lcs = sequences[combo[0]]
            for i in range(1, len(combo)):
                current_lcs = find_lcs_pair(current_lcs, sequences[combo[i]])

                # Verify this LCS appears in all sequences in the combination
            is_valid = True
            for idx in combo:
                if not is_subsequence(current_lcs, sequences[idx]):
                    is_valid = False
                    break

            if not is_valid:
                continue

                # Update if this is a better solution
                # Prefer more sequences when lengths are equal
            if (len(current_lcs) > len(max_lcs)) or \
                    (len(current_lcs) == len(max_lcs) and len(combo) > max_sequence_count):
                max_lcs = current_lcs
                max_indices = [i + 1 for i in combo]  # Convert to 1-based indexing
                max_sequence_count = len(combo)

        return {
            "value": max_lcs,
            "sequences": max_indices,
            "length": len(max_lcs)
        }


def is_subsequence(shorter, longer):
    """Check if shorter is a subsequence of longer."""
    if not shorter:
        return True

    j = 0  # Index for shorter
    for i in range(len(longer)):
        if longer[i] == shorter[j]:
            j += 1
            if j == len(shorter):
                return True
    return False

def process_sequence(sequence):
    """
    Process a single DNA sequence to calculate its GC content and codon frequency.

    :param sequence: A string representing the DNA sequence.
    :return: A dictionary with:
        - "gc_content": The GC content percentage of the sequence.
        - "codons": A dictionary where keys are codons (triplets) and values are their frequencies.
    """
    logging.debug("Processing individual sequence.")
    gc_content = calc_gc_content(sequence)
    codons_frequency = compute_codon_frequency(sequence)
    return {"gc_content": gc_content, "codons": codons_frequency}


def process_txt_files(txt_file_path):
    """
    Process DNA sequences in the .txt file.

    :param txt_file_path: Path to the .txt file.
    :return: Processed results including GC content, codon frequency, and LCS.
    """
    logging.info(f"Processing TXT file: {txt_file_path}")
    with open(txt_file_path, 'r') as file: # remove trailing and leading blanks
        sequences = [line.strip() for line in file if line.strip()]

    logging.debug(f"Read {len(sequences)} sequences from {txt_file_path}")

    # Use multiprocessing to process sequences in parallel
    with Pool(processes=cpu_count()) as pool:
        sequence_results = pool.map(process_sequence, sequences)

    # compute most common codon and lcs
    most_common_codon = compute_most_frequent_codon(sequences)
    lcs_result = compute_longest_common_subsequence(sequences)

    logging.info("Completed processing TXT file.")
    return {
        "sequences": sequence_results,
        "most_common_codon": most_common_codon,
        "lcs":
            lcs_result
    }





















