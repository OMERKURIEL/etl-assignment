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
    Compute the most frequent codon across the DNA sequences.

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
    # compute the frequency of the most common codon
    max_frequency = max(total_codon_count.values())
    # in case of more than one most frequent codon, find all of them
    most_frequent_codons = [
        codon for codon, count in total_codon_count.items()
        if count == max_frequency
    ]
    # join the results to the expected format
    results = ", ".join(most_frequent_codons)
    logging.debug(f"most frequent codon: {most_frequent_codons}.")
    return results


def find_lcs_of_two(sequence1, sequence2):
    """
    Helper function - Find the longest common contiguous substring between two sequences.

    :param sequence1: A string representing the first DNA sequence.
    :param sequence2: A string representing the second DNA sequence.
    """
    n, m = len(sequence1), len(sequence2)
    longest_sub = ""
    # Try all possible starting positions in sequence1
    for i in range(n):
        # For each starting position, try increasing lengths
        for length in range(1, n - i + 1):
            current_sub = sequence1[i:i + length]
            # If this substring appears in sequence2 and is longer than current best, replace it
            if current_sub in sequence2 and len(current_sub) > len(longest_sub):
                longest_sub = current_sub
    return longest_sub


def process_lcs_pair(pair):
    """
    Helper function for multiprocessing: Compute LCS for a sequence pair.

    :param pair: A pair of strings representing the DNA sequences.
    :return: A string representing the LCS of the pair.
    """
    seq1, seq2 = pair
    lcs = find_lcs_of_two(seq1, seq2)
    return lcs

def compute_longest_common_subsequence(sequences):
    """
    Compute the longest frequent codon across the DNA sequences.
    The longest common subsequence is defined as the longest common subsequence of any sequence combination.
    (not necessarily common to all sequences).

    :param sequences: A list of strings, each representing a DNA sequence.
    :return: The most frequent codon as a string.
    """
    if not sequences:
        return {"value": "", "sequences": [], "length": 0}

    # Generate all possible sequence pairs with their indices, and Use multiprocessing for efficiency
    sequence_pairs = [(sequences[i], sequences[j]) for i, j in combinations(range(len(sequences)), 2)]
    with Pool(processes=cpu_count()) as pool:
        lcs_results = pool.map(process_lcs_pair, sequence_pairs)

    # Track all candidates of maximum length
    max_length = 0
    candidates = []

    # find the maximum length from the subsequences found
    for lcs in lcs_results:
        if lcs and len(lcs) >= max_length:
            if len(lcs) > max_length:
                max_length = len(lcs)
                candidates = [] # longer subsequence found, reset the candidates list
            candidates.append(lcs)

    candidates = list(dict.fromkeys(candidates)) # Remove duplicates

    # If no common substrings found
    if not candidates:
        return {"value": "", "sequences": [], "length": 0}

    max_occurrences = 0
    best_results = {}  # store all lcs that have the same length and frequency

    # For each candidate, find all sequences it appears in
    for candidate in candidates:
        sequence_indices = [i + 1 for i, seq in enumerate(sequences) if candidate in seq]
        current_occurrences = len(sequence_indices)

        if current_occurrences >= max_occurrences:
            if current_occurrences > max_occurrences: # New maximum found, reset candidates dict
                max_occurrences = current_occurrences
                best_results = {}

            # Add this candidate's complete result
            best_results[candidate] = {
                "value": candidate,
                "sequences": sequence_indices,
                "length": len(candidate)
            }
    # If only one candidate, return it directly
    if len(best_results) == 1:
        return next(iter(best_results.values()))

    # If multiple candidates, return dictionary of all results
    return best_results


def process_sequence(sequence):
    """
    Helper function for multiprocessing:
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

    if not sequences:
        logging.error(f"Validation Error: TXT file {txt_file_path} is empty.")
        raise ValueError(f"TXT file {txt_file_path} is empty.")

    logging.debug(f"Read {len(sequences)} sequences from {txt_file_path}")

    # Use multiprocessing to process sequences in parallel
    with Pool(processes=cpu_count()) as pool:
        sequences_results = pool.map(process_sequence, sequences)

    # compute most common codon and lcs
    most_common_codon = compute_most_frequent_codon(sequences)
    lcs_result = compute_longest_common_subsequence(sequences)

    logging.info("Completed processing TXT file.")
    return {
        "sequences": sequences_results,
        "most_common_codon": most_common_codon,
        "lcs":
            lcs_result
    }





















