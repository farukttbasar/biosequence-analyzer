import argparse

# ARGPARSE
def parser_cli():
    parser = argparse.ArgumentParser(
        description="-- BioSequence Analyzer CLI --\n"
        "A CLI tool for analyzing, converting, and generating DNA/RNA sequences."
    )

    parser.add_argument(
        "-s",
        "--sequence",
        type=str,
        help="Enter DNA or RNA sequence string (e.g ATGCCGTAG)"
    )

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["dna", "rna"],
        default="dna",
        help="Type of the sequence: dna or rna (default: dna)"
    )

    parser.add_argument(
        "--action",
        choices=[1, 2, 3, 4, 5, 6],
        type=int,
        default=5,
        help="Analyse action: 1. gc_ratio, 2. frequencies, 3. complement, 4. convert, 5. all, 6. compare (default: 5)"
    )

    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Generate a random sequence instead of providing manually."
    )

    parser.add_argument(
        "-c2",
        "--compare-with",
        type=str,
        help="Second sequence string to compare with the primary sequence."
    )

    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=50,
        help="Length of a random sequence (default: 50)",
    )

    parser.add_argument(
        "-g",
        "--gc-ratio",
        type=float,
        default=0.5,
        help="GC ratio for the random sequence between 1.0 - 0.0 (inclusive)"
    )

    return parser.parse_args()

# INTERACTIVE INPUT

def get_input(prompt, error_message, targetted_type, default=None, validator=None):
    while True:
        first_val = input(prompt + " > ").strip()

        if not first_val and default is not None:
            return default
        
        try:
            val = targetted_type(first_val)
            if validator and not validator(val):
                raise ValueError
            return val
        except ValueError:
            print(error_message)

def get_interactive_input():
    print("=" * 40)
    print("--- BioSequence Analyzer ---")
    print("=" * 40)

    is_random = get_input(
        "Generate a random sequence? (y / n, default: n)",
        "Please enter 'y' or 'n'!",
        str,
        default="n",
        validator=lambda x: x.lower() in ["y", "n"]
    ).lower().strip()

    is_random = is_random == "y"

    seq_type = get_input(
        "Sequence type: DNA or RNA (default: dna)",
        "Please enter 'dna' or 'rna'!",
        str,
        default="dna",
        validator=lambda x: x.lower() in ["dna", "rna"]
    ).lower()

    sequence = None
    length = 50
    gc_ratio = 0.5

    if is_random:
        length = get_input(
            "Enter sequence length (default: 50)",
            "Please enter a positive integer!",
            int,
            default=50,
            validator=lambda x: x > 0
        )

        gc_ratio = get_input(
            "Enter GC ratio between 1.0 - 0.0 (default: 0.5)",
            "Please enter a ratio between 1.0 - 0.0!",
            float,
            default=0.5,
            validator=lambda x: 0.0 <= x <= 1.0
        )
    else:
        valid_bases = {"A", "T", "G", "C"} if seq_type == "dna" else {"A", "U", "G", "C"}
        sequence = get_input(
            f"Enter a {seq_type.upper()} sequence",
            f"Valid bases are {valid_bases} for {seq_type.upper()}",
            str,
            validator=lambda x: len(x) > 0 and set(x.upper()).issubset(valid_bases)
        ).upper()

    print("\n--- ACTIONS ---")
    print("1. Calculate GC Content")
    print("2. Calculate Base Frequency")
    print("3. Find the Complement")
    print("4. Convert (DNA <=> RNA)")
    print("5. All Analyses (1 to 4)")
    print("6. Compare Sequences")


    choice = get_input(
        "Select an action (default: '5. All')",
        "Please select between 1 - 6 (inclusive)!", 
        int,
        default=5,
        validator=lambda x: 1 <= x <= 6 
    )

    compare_with = None

    if choice == 6:
        compare_with = get_input(
            f"Enter second {seq_type.upper()} sequence for comparison",
            f"Valid bases are {valid_bases} for {seq_type.upper()}",
            str,
            validator=lambda x: len(x) > 0 and set(x.upper()).issubset(valid_bases)
        ).upper()

    return argparse.Namespace(
        sequence = sequence,
        type = seq_type,
        action = choice,
        random = is_random,
        length = length,
        gc_ratio = gc_ratio,
        compare_with=compare_with
    )    