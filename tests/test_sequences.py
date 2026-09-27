import pytest
from source.sequence import DNASequence, RNASequence, BaseSequence

# RANDOM CREATING TESTS
def test_create_random_dna():
    length = 2000 # Used 2000 to avoid flaky test failures from variance.
    dna = DNASequence.create_random(length=length, gc_content=0.5)
    assert isinstance(dna, DNASequence)
    assert len(dna) == 2000
    assert "U" not in dna.sequence
    assert dna.name.startswith("RANDOM-DNA")

    actual_dna_gc_content = (dna.sequence.count("G") + dna.sequence.count("C")) / length
    assert actual_dna_gc_content == pytest.approx(0.5, abs=0.08)

def test_create_random_rna():
    length = 2000 # Used 2000 to avoid flaky test failures from variance.
    rna = RNASequence.create_random(length=length, gc_content=0.5)
    assert isinstance(rna, RNASequence)
    assert len(rna) == 2000
    assert "T" not in rna.sequence
    assert rna.name.startswith("RANDOM-RNA")

    actual_rna_gc_content = (rna.sequence.count("G") + rna.sequence.count("C")) / length
    assert actual_rna_gc_content == pytest.approx(0.5, abs=0.08)

def test_create_random_invalid_length_raises_error():
    with pytest.raises(ValueError):
        DNASequence.create_random(length=-50)
        RNASequence.create_random(length=-50)

def test_create_random_invalid_gc_content_raises_error():
    with pytest.raises(ValueError):
        DNASequence.create_random(gc_content=1.5)
        RNASequence.create_random(gc_content=1.5)

def test_create_random_invalid_class_raises_error():
    with pytest.raises(TypeError):
        BaseSequence.create_random(length=100, gc_content=0.5)
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
