import pytest
from source.sequence import DNASequence, RNASequence
from source.calculations import (
    calculate_gc_content,
    calculate_base_frequency,
    compare_sequences
)

# GC CONTENT TESTS
@pytest.mark.parametrize("seq_cls, raw_seq, expected_gc", [
    (DNASequence, "GGCC", 100.0),
    (DNASequence, "CGTAGC", 66.67),
    (DNASequence, "ATGC", 50.0),
    (DNASequence, "AAAA", 0.0),
    (RNASequence, "GGCC", 100.0),
    (RNASequence, "GCAUCG", 66.67),
    (RNASequence, "AUGC", 50.0),
    (RNASequence, "UUUU", 0.0),
])
def test_calculate_gc_content(seq_cls, raw_seq, expected_gc):
    obj = seq_cls(sequence=raw_seq)
    assert calculate_gc_content(obj) == expected_gc

@pytest.mark.parametrize("invalid_input", ["ATGC", "AUGC",])
def test_gc_calculate_invalid_input_raises_error(invalid_input):
    with pytest.raises(TypeError):
        calculate_gc_content(invalid_input)

# BASE FREQUENCY TESTS
@pytest.mark.parametrize("seq_cls, raw_seq, the_different_base", [
    (DNASequence, "CGTAGC", "T"),
    (RNASequence, "GCAUCG", "U"),
])
def test_calculate_base_frequency(seq_cls, raw_seq, the_different_base):
    obj = seq_cls(sequence=raw_seq)
    frequencies = calculate_base_frequency(obj)

    assert frequencies["A"] == round(1 / 6, 4)
    assert frequencies[the_different_base] == round(1 / 6, 4)
    assert frequencies["G"] == round(2 / 6, 4)
    assert frequencies["C"] == round(2 / 6, 4)

@pytest.mark.parametrize("invalid_input", ["ATGC", "AUGC"])
def test_base_frequency_invalid_input_raises_error(invalid_input):
    with pytest.raises(TypeError):
        calculate_base_frequency(invalid_input)

# COMPARE SEQUENCES TESTS
@pytest.mark.parametrize("seq_cls, seq1_str, seq2_str, expected_matches, expected_mismatches", [
    (DNASequence, "ATGC", "ATGC", 4, 0),
    (DNASequence, "ATGC", "ATCC", 3, 1),
    (DNASequence, "AAAA", "TTTT", 0, 4),
    (RNASequence, "AUGC", "AUGC", 4, 0),
    (RNASequence, "AUGC", "AUCC", 3, 1),
    (RNASequence, "AAAA", "UUUU", 0, 4),
])
def test_compare_sequences(seq_cls, seq1_str, seq2_str, expected_matches, expected_mismatches):
    seq1 = seq_cls(sequence=seq1_str)
    seq2 = seq_cls(sequence=seq2_str)
    result = compare_sequences(seq1, seq2)

    assert result["Length"] == len(seq1_str)
    assert result["Matches"] == expected_matches
    assert result["Mismatches"] == expected_mismatches

@pytest.mark.parametrize("seq_cls, seq1_str, seq2_str", [
    (DNASequence, "ATGC", "ATC"),
    (RNASequence, "AUGC", "AUC"),
    (DNASequence, "A", "AA"),
    (RNASequence, "A", "AA"),
])
def test_compare_sequences_not_equal_length_raises_error(seq_cls, seq1_str, seq2_str):
    seq1 = seq_cls(seq1_str)
    seq2 = seq_cls(seq2_str)
    with pytest.raises(ValueError):
        compare_sequences(seq1, seq2)

@pytest.mark.parametrize("seq_cls, valid_seq", [
    (DNASequence, "ATGC"),
    (RNASequence, "AUGC"),
])
def test_compare_type_error(seq_cls, valid_seq):
    obj = seq_cls(sequence=valid_seq)

    with pytest.raises(TypeError):
        compare_sequences(obj, valid_seq)

    with pytest.raises(TypeError):
        compare_sequences(valid_seq, obj)
