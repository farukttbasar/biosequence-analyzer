import pytest
from source.sequence import DNASequence, RNASequence, BaseSequence

# RANDOM CREATING TESTS
@pytest.mark.parametrize("seq_cls, prefix, invalid_base", [
    (DNASequence, "RANDOM-DNA", "U"),
    (RNASequence, "RANDOM-RNA", "T"),
])
def test_create_random_sequence(seq_cls, prefix, invalid_base):
    length = 2000 # Used 2000 to avoid flaky test failures from variance.
    seq = seq_cls.create_random(length=length, gc_content=0.5)

    assert isinstance(seq, seq_cls)
    assert len(seq) == length
    assert invalid_base not in seq.sequence
    assert seq.name.startswith(prefix)

@pytest.mark.parametrize("seq_cls" ,[DNASequence, RNASequence])
@pytest.mark.parametrize("invalid_length" ,[0, -100, -150])
def test_create_random_invalid_length_raises_error(seq_cls, invalid_length):
    with pytest.raises(ValueError):
        seq_cls.create_random(length=invalid_length)

@pytest.mark.parametrize("seq_cls" ,[DNASequence, RNASequence])
@pytest.mark.parametrize("invalid_gc_content" ,[-0.5, 1.5])
def test_create_random_invalid_gc_content_raises_error(seq_cls, invalid_gc_content):
    with pytest.raises(ValueError):
        seq_cls.create_random(gc_content=invalid_gc_content)

def test_create_random_invalid_class_type_raises_error():
    with pytest.raises(TypeError):
        BaseSequence.create_random(length=100, gc_content=0.5)

# SEQUENCE CREATION TESTS
@pytest.mark.parametrize("seq_cls, raw_seq, custom_name, expected_prefix", [
    (DNASequence, "ATGC", "Sample_DNA", "DNA"),
    (RNASequence, "AUGC", "Sample_RNA", "RNA"),
])
def test_sequence_creation_with_custom_name(seq_cls, raw_seq, custom_name, expected_prefix):
    obj = seq_cls(sequence=raw_seq, name=custom_name)

    assert obj.sequence == raw_seq
    assert obj.name == custom_name
    assert len(obj) == 4
    assert obj.prefix == expected_prefix

@pytest.mark.parametrize("seq_cls, raw_seq, expected_prefix", [
    (DNASequence, "ATGC", "DNA"),
    (RNASequence, "AUGC", "RNA"),
])
def test_sequence_creation_default_name(seq_cls, raw_seq, expected_prefix):
    obj = seq_cls(sequence=raw_seq)
    assert obj.sequence == raw_seq
    assert obj.name.startswith(f"{expected_prefix}-")
    assert len(obj.name.split("-")[1]) == 3

@pytest.mark.parametrize("seq_cls, raw_seq", [
    (DNASequence, "ATGC"),
    (RNASequence, "AUGC"),
])
def test_sequence_creation_blank_name_raises_error(seq_cls, raw_seq):
    with pytest.raises(ValueError):
        seq_cls(sequence=raw_seq, name="  ")

@pytest.mark.parametrize("seq_cls, invalid_raw_seq", [
    (DNASequence, "ATGCU"),
    (DNASequence, "ATGCL"),
    (DNASequence, "ATGC1"),
    (DNASequence, "1234"),
    (RNASequence, "AUGCT"),
    (RNASequence, "AUGCL"),
    (RNASequence, "AUGC1"),
    (RNASequence, "1234"),
])
def test_sequence_creation_invalid_sequence_raises_error(seq_cls, invalid_raw_seq):
    with pytest.raises(ValueError):
        seq_cls(sequence=invalid_raw_seq)

@pytest.mark.parametrize("seq_cls, empty_raw_seq", [
    (DNASequence, ""),
    (DNASequence, "   "),
    (RNASequence, ""),
    (RNASequence, "   "),
])
def test_empty_sequence_raises_error(seq_cls, empty_raw_seq):
    with pytest.raises(ValueError):
        seq_cls(sequence=empty_raw_seq)

@pytest.mark.parametrize("seq_cls, raw_seq", [
    (DNASequence, "ATGC" * 20),
    (RNASequence, "AUGC" * 20,)
])
def test_sequence_str_fasta_representation(seq_cls, raw_seq):
    obj = seq_cls(sequence=raw_seq, name="FASTA_TEST")
    fasta_type = str(obj)
    assert fasta_type.startswith(">FASTA_TEST\n")
    lines = fasta_type.split("\n")
    assert len(lines[1]) == 60
    assert len(lines[2]) == 20

# COMPLEMENT AND TRANSITION TESTS
@pytest.mark.parametrize("seq_cls, raw_seq, expected_complement", [
    (DNASequence, "ATGC", "TACG"),
    (RNASequence, "AUGC", "UACG"),
    (DNASequence, "AATTGGCC", "TTAACCGG"),
    (RNASequence, "AAUUGGCC", "UUAACCGG"),
])
def test_complement(seq_cls, raw_seq, expected_complement):
    obj = seq_cls(sequence=raw_seq)
    assert obj.complement() == expected_complement

def test_dna_transcription_to_rna():
    dna = DNASequence(sequence="ATGC")
    rna = dna.to_rna()
    assert isinstance(rna, RNASequence)
    assert rna.sequence == "AUGC"
    assert rna.name.startswith("DNA-RNA-")


def test_rna_reverse_transcription_to_dna():
    rna = RNASequence(sequence="AUGC")
    dna = rna.to_dna()
    assert isinstance(dna, DNASequence)
    assert dna.sequence == "ATGC"
    assert dna.name.startswith("RNA-DNA-")


