import pytest
from source.sequence import DNASequence, RNASequence

# DNA TESTS

def test_dna_creation(sample_dna):
    assert sample_dna.sequence == "ATGC"
    assert sample_dna.name == "Sample_DNA"
    assert sample_dna.prefix == "DNA"
    assert len(sample_dna) == 4

def test_invalid_dna_raises_error():
    with pytest.raises(ValueError):
        DNASequence(sequence="ATGCU")

def test_empty_sequence_raises_error():
    with pytest.raises(ValueError):
        DNASequence(sequence="")

def test_complement(sample_dna):
    assert sample_dna.complement() == "TACG"

def test_transcription_to_rna(sample_dna):
    rna = sample_dna.to_rna()
    assert isinstance(rna, RNASequence)
    assert rna.sequence == "AUGC"

# RNA TESTS

def test_rna_creation(sample_rna):
    assert sample_rna.sequence == "AUGC"
    assert sample_rna.name == "Sample_RNA"
    assert len(sample_rna) == 4

def test_invalid_rna_raises_error():
    with pytest.raises(ValueError):
        RNASequence(sequence="AUGCT")

def test_empty_sequence_raises_error():
    with pytest.raises(ValueError):
        RNASequence(sequence="")

def test_complement(sample_rna):
    assert sample_rna.complement() == "UACG"

def test_reverse_transvription_to_dna(sample_rna):
    dna = sample_rna.to_dna()
    assert isinstance(dna, DNASequence)
    assert dna.sequence == "ATGC"
