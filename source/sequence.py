import textwrap
import random

class BaseSequence:
    counter = 0
    prefix = "SEQ"
    valid_bases = frozenset()

    def __init__(self, sequence, name=None):
        if sequence.strip() == "":
            raise ValueError("Sequence cannot be empty")
        else:
            self.sequence = sequence

        self.__class__.counter += 1

        if name is None:
            self.name = f"{self.__class__.prefix}-{self.__class__.counter:03d}"
        elif name.strip() == "":
            raise ValueError("Sequence name cannot be empty.")
        else:
            self.name = name

    def __len__ (self):
        return len(self._sequence)

    def count_base(self, base):
        return self._sequence.count(base)

    def base_counts(self):
        return {base: self._sequence.count(base) for base in self.valid_bases}

    @classmethod
    def create_random(cls, length=100, gc_content=0.5, name=None):
        if length <= 0:
            raise ValueError("Sequence length must be positive.")
        if not (0.0 <= gc_content <= 1):
            raise ValueError("GC content must be between 0.0 - 1.0.")

        probability_g = gc_content / 2.00
        probability_c = gc_content / 2.00
        probability_others = (1.00 - gc_content) / 2.00

        if "T" in cls.valid_bases:
            bases = ["A", "T", "G", "C"]
            prob = [probability_others, probability_others, probability_g, probability_c]
        elif "U" in cls.valid_bases:
            bases = ["A", "U", "G", "C"]
            prob = [probability_others, probability_others, probability_g, probability_c]
        else:
            raise TypeError(f"Creating random sequence is not available for the class {cls.__name__}.")

        raw_sequence = "".join(random.choices(bases, weights=prob, k=length))

        next_counter = cls.counter + 1
        random_name = f"RANDOM-{cls.prefix}-{next_counter:03d}"
        return cls(raw_sequence, name=random_name)

    def __str__(self):
        wrapped_sequence = textwrap.fill(self._sequence, width=60)
        return f">{self.name}\n{wrapped_sequence}"

    # sequence getter
    @property
    def sequence(self):
        return self._sequence

    # sequence setter
    @sequence.setter
    def sequence(self, sequence):
        for base in sequence:
            if base not in self.valid_bases:
                raise ValueError("Please provide a valid sequence. ")
        self._sequence = sequence

class DNASequence(BaseSequence):
    counter = 0
    prefix = "DNA"
    valid_bases = frozenset(["A", "T", "G", "C"])

    def complement(self):
        complement_bases = {"A": "T", "T": "A", "G": "C", "C": "G"}
        new_sequence = ""

        for base in self.sequence:
            new_sequence += complement_bases[base]

        return new_sequence

    def to_rna(self, rna_name=None):
        rna_sequence = self.sequence.replace("T", "U")

        if rna_name is None:
            next_rna_no = RNASequence.counter + 1
            rna_name = f"{self.prefix}-RNA-{next_rna_no:03d}"

        return RNASequence(rna_sequence, rna_name)
 

class RNASequence(BaseSequence):
    counter = 0
    prefix = "RNA"
    valid_bases = frozenset(["A", "U", "G", "C"])

    def complement(self):
        complement_bases = {"A": "U", "U": "A", "G": "C", "C": "G"}
        new_sequence = ""

        for base in self.sequence:
            new_sequence += complement_bases[base]

        return new_sequence

    def to_dna(self, dna_name=None):
        dna_sequence = self.sequence.replace("U", "T")

        if dna_name is None:
            next_dna_no = DNASequence.counter + 1
            dna_name = f"{self.prefix}-DNA-{next_dna_no:03d}"

        return DNASequence(dna_sequence, dna_name)

