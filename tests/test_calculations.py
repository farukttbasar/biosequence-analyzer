import pytest
from source.sequence import DNASequence, RNASequence
from source.calculations import (
    calculate_gc_content,
    calculate_base_frequency,
    compare_sequences
)

# DNA TESTS 

def test_gc_content(dna_seq):
    assert calculate_gc_content(dna_seq) == 66.67

def test_dna_gc_calculate_type_error():
    with pytest.raises(TypeError):
        calculate_gc_content("ATGC")

def test_dna_calculate_base_frequency(dna_seq):
    frequencies = calculate_base_frequency(dna_seq)
    assert frequencies["A"] == round(1/6, 4)
    assert frequencies["T"] == round(1/6, 4)
    assert frequencies["G"] == round(2/6, 4)
    assert frequencies["C"] == round(2/6, 4)

def test_dna_compare_sequences():
    seq1 = DNASequence(sequence="ATGC")
    seq2 = DNASequence(sequence="ATCC")

    result = compare_sequences(seq1, seq2)

    assert result["Length"] == 4
    assert result["Matches"] == 3
    assert result["Mismatches"] == 1

def test_dna_compare_sequences_not_equal_raises_error():
    seq1 = DNASequence("ATGC")
    seq2 = DNASequence("ATC")

    with pytest.raises(ValueError):
        compare_sequences(seq1, seq2)

def test_dna_compare_type_error():
    with pytest.raises(TypeError):
        compare_sequences(DNASequence(sequence="ATGC"), "ATGC")

    with pytest.raises(TypeError):
        compare_sequences("ATGC", DNASequence(sequence="ATGC"))

# RNA TESTS

def test_rna_gc_content(rna_seq):
    assert calculate_gc_content(rna_seq) == 66.67

def test_rna_gc_calculate_type_error():
    with pytest.raises(TypeError):
        calculate_gc_content("AUGC")

def test_rna_calculate_base_frequency(rna_seq):
    frequencies = calculate_base_frequency(rna_seq)
    assert frequencies["A"] == round(1/6, 4)
    assert frequencies["U"] == round(1/6, 4)
    assert frequencies["G"] == round(2/6, 4)
    assert frequencies["C"] == round(2/6, 4)

def test_rna_compare_sequences():
    seq1 = RNASequence(sequence="AUGC")
    seq2 = RNASequence(sequence="AUCC")

    result = compare_sequences(seq1, seq2)

    assert result["Length"] == 4
    assert result["Matches"] == 3
    assert result["Mismatches"] == 1

def test_rna_compare_sequences_not_equal_raises_error():
    seq1 = RNASequence(sequence="AUGC")
    seq2 = RNASequence(sequence="AUC")

    with pytest.raises(ValueError):
        compare_sequences(seq1, seq2)

def test_rna_compare_type_error():
    with pytest.raises(TypeError):
        compare_sequences(RNASequence(sequence="AUGC"), "AUGC")

    with pytest.raises(TypeError):
        compare_sequences("AUGC", RNASequence(sequence="AUGC"))
