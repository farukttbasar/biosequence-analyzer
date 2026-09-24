import pytest
from source.sequence import DNASequence, RNASequence

@pytest.fixture
def sample_dna():
    return DNASequence(sequence="ATGC", name="Sample_DNA")

@pytest.fixture
def sample_rna():
    return RNASequence(sequence="AUGC", name="Sample_RNA")

@pytest.fixture
def dna_seq():
    return DNASequence(sequence="CGTAGC")

@pytest.fixture
def rna_seq():
    return RNASequence(sequence="GCAUCG")

