from source.sequence import DNASequence, RNASequence
from source.cli import parser_cli, get_interactive_input
from source.calculations import (
    calculate_gc_content,
    calculate_base_frequency,
    compare_sequences
)

def run_calculations(seq_obj, action):
    print(f"🧬 Working on {seq_obj.name}")
    print(f"Sequence ({seq_obj.sequence})")
    print("=" * 50)

    if action == 5 or action == 1:
        gc_ratio = calculate_gc_content(seq_obj)
        print(f"> GC Content: {gc_ratio:.2f} %\n")

    if action == 5 or action == 2:
        base_freq = calculate_base_frequency(seq_obj)
        counts = seq_obj.base_counts()

        print(f"> Base Frequencies: ")
        print(f"   {'Base':<4} {'Count':<10} {'Frequency':<12}")
        print("   " + "-" * 28)
        for base in seq_obj.valid_bases:
            print(f"   {base:<4} {counts.get(base, 0):<10} {base_freq.get(base, 0.0):<12.4f}")
        print("\n")

    if action == 5 or action == 3:
        print(f"> Complement: {seq_obj.complement()}\n")

    if action == 5 or action == 4:
        if isinstance(seq_obj, DNASequence):
            print(f"> Transcription (DNA => RNA): {seq_obj.to_rna().sequence}\n")
        else:
            print(f"> Reverse Transcription (RNA => DNA): {seq_obj.to_dna().sequence}\n")

    print("=" * 50)

def main():
    args = parser_cli()

    if not args.random and not args.sequence:
        args = get_interactive_input()

    seq_class = DNASequence if args.type == "dna" else RNASequence

    try:
        if args.random:
            print(f"Generating a random {args.type.upper()} sequence (Length: {args.length}, GC Ratio: {args.gc_ratio})")
            seq_obj = seq_class.create_random(args.length, args.gc_ratio)
        else:
            seq_obj = seq_class(args.sequence.upper())

        run_calculations(seq_obj, args.action)
    except (ValueError, TypeError) as e:
        print(f"Error --> {e}")

if __name__ == "__main__":
    main()

