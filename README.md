# BioSequence Analyzer

A modular DNA/RNA sequence analysis written in Python.

## Features

- **Object-Oriented Representation**: Sequence modeling with `BaseSequence`, `DNASequence`, and `RNASequence`.
- **Validation**: Validation of nucleotide bases using `@property` setters and frozen sets.
- **Biochemical Calculations**:
  - GC-content percentage calculation
  - Relative nucleotide base frequency calculation
  - Pairwise sequence alignment and match/mismatch verification
  - Transcription (DNA -> RNA) and reverse transcription (RNA -> DNA)
- **FASTA Export**: Automatic text formatting compliant with standard FASTA line wrapping (60 characters).

## Quickstart

Run the interactive console program:

```bash
python main.py
