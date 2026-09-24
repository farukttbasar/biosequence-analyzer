from source.sequence import BaseSequence

def calculate_gc_content(seq_obj):
    if not isinstance(seq_obj, BaseSequence):
        raise TypeError("Expected an instance of BaseSequence.")
    
    total_length = len(seq_obj)
    if total_length == 0:
        return 0.0

    g_count = seq_obj.count_base("G")
    c_count = seq_obj.count_base("C")

    gc_percentage = ((g_count + c_count) / total_length) * 100
    return round(gc_percentage,2)

def calculate_base_frequency(seq_obj):
    if not isinstance(seq_obj, BaseSequence):
        raise TypeError("Expected an instance of BaseSequence.")

    total_length = len(seq_obj)
    if total_length == 0:
        return {base: 0.0 for base in seq_obj.valid_bases}

    counts = seq_obj.base_counts()
    frequencies = {base: round(count/total_length, 4) for base, count in counts.items()}

    return frequencies

def compare_sequences(seq1, seq2):
    if not (isinstance(seq1, BaseSequence) and isinstance(seq2, BaseSequence)):
        raise TypeError("Expected an instance of BaseSequence.")

    if len(seq1) != len(seq2):
        raise ValueError(f"Sequences must have the same length! {seq1.name}: {len(seq1)} | {seq2.name}: {len(seq2)}")

    total_component = len(seq1)
    if total_component == 0:
        return {
            "Length": 0,
            "Matches": 0,
            "Mismatches": 0,
        }

    matches = 0
    mismatches = 0

    for base1, base2 in zip(seq1.sequence, seq2.sequence):
        if base1 == base2:
            matches += 1
        else:
            mismatches += 1

    return {
        "Length": total_component,
        "Matches": matches,
        "Mismatches": mismatches
    }