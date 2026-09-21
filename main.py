from sequence import DNASequence, RNASequence
from calculations import (
    calculate_gc_content,
    calculate_base_frequency,
    compare_sequences
)

def show_menu():
    print("\n" + "=" * 35)
    print("      SEQUENCE ANALYSIS SYSTEM      ")
    print("=" * 35)
    print("| 1. Create DNA sequence            |")
    print("| 2. Create RNA sequence            |")
    print("| 3. Show sequence (FASTA)          |")
    print("| 4. Count bases & frequencies      |")
    print("| 5. Calculate GC content           |")
    print("| 6. Find complement                |")
    print("| 7. Convert sequence (DNA <-> RNA) |")
    print("| 8. Compare sequences              |")
    print("| 9. Exit                           |")
    print("=" * 35)

def select_sequence(sequences, prompt="Select a sequence > "):
    if not sequences:
        print("No sequences found in the system.")
        return None
    
    print("\n--- Registered Sequences ---")
    keys = list(sequences.keys())

    for idx, key in enumerate(keys, 1): # idx= 1,2,3,... | key= DNA-001, RNA-002, ...
        seq = sequences[key]
        print(f"{idx}. {seq.name} ({seq.__class__.__name__}) [Length: {len(seq)}]")

    choice = input(prompt).strip()
    if choice.isdigit() and 1 <= int(choice) <= len(keys):
        return sequences[keys[int(choice) - 1]]
    elif choice in sequences:
        return sequences[choice]
    else:
        print("Invalid selection. Please try again.")
        return None

def main():
    sequences = {}

    while True:
        show_menu()
        choice = input("Please select an option (1-9): ").strip()

        if choice == "1":
            try:
                dna_seq_str = input("Enter DNA sequence (A, T, G, C) > ").strip().upper()
            except ValueError as e:
                print(f"Error: {e}")
            dna_name_str = input("Enter a sequence name (Optional, press Enter to skip) > ").strip()
            name = dna_name_str if dna_name_str else None

            try:
                dna = DNASequence(dna_seq_str, name)
                sequences[dna.name] = dna
                print(f"DNA sequence created successfully: {dna.name}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            rna_seq_str = input("Enter RNA sequence (A, U, G, C) > ").strip().upper()
            rna_name_str = input("Enter a sequence name (Optional, press Enter to skip) > ").strip()
            name = rna_name_str if rna_name_str else None

            try:
                rna = RNASequence(rna_seq_str, name)
                sequences[rna.name] = rna
                print(f"RNA sequence created successfully: {rna.name}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            seq_obj = select_sequence(sequences)

            if seq_obj:
                print("\n--- FASTA Format ---")
                print(seq_obj)

        elif choice == "4":
            seq_obj = select_sequence(sequences)
            if seq_obj:
                counts = seq_obj.base_counts()
                frequencies = calculate_base_frequency(seq_obj)
                print(f"{'Base':<6} {'Count':<8} {'Frequency (Ratio)':<18}")
                print("-" * 34)
                for base in seq_obj.valid_bases:
                    count = counts.get(base, 0)
                    freq = frequencies.get(base, 0.0)
                    print(f"{base:<6} {count:<8} {freq:<18.4f}")

        elif choice == "5":
            seq_obj = select_sequence(sequences)
            if seq_obj:
                gc = calculate_gc_content(seq_obj)
                print(f"{seq_obj.name} GC CONTENT: {gc}%")

        elif choice == "6":
            seq_obj = select_sequence(sequences)
            if seq_obj:
                if isinstance(seq_obj, DNASequence):
                    comp_seq_str = seq_obj.complement()
                    print(f"\nOriginal: {seq_obj.sequence}")
                    print(f"Complement: {comp_seq_str}")
                else:
                    print("Error: The complement operation is only supported for DNA sequences.")

        elif choice == "7":
            seq_obj = select_sequence(sequences, "Select a sequence to convert > ")
            if seq_obj:
                if isinstance(seq_obj, DNASequence):
                    converted_obj = seq_obj.to_rna()
                    sequences[converted_obj.name] = converted_obj
                    print("\nTranscription (DNA -> RNA) successful!")
                    print(f"New RNA Object : {converted_obj.name}")
                    print(f"RNA Sequence   : {converted_obj.sequence}")

                elif isinstance(seq_obj, RNASequence):
                    converted_obj = seq_obj.to_dna()
                    sequences[converted_obj.name] = converted_obj
                    print("\nReverse Transcription (RNA -> DNA) successful!")
                    print(f"New DNA Object : {converted_obj.name}")
                    print(f"DNA Sequence   : {converted_obj.sequence}")

        elif choice == "8":
            if len(sequences) < 2:
                print("You must have at least 2 registered sequences to perform a comparison.")
                continue

            print("\nSelect sequence 1 > ")
            seq1 = select_sequence(sequences)
            if not seq1:
                continue

            print("\nSelect sequence 2 >")
            seq2 = select_sequence(sequences)
            if not seq2:
                continue

            try:
                result = compare_sequences(seq1, seq2)
                print(f"\n--- Comparison Result ({seq1.name} vs {seq2.name}) ---")
                print(f"Total Length : {result['Length']}")
                print(f"Matches      : {result['Matches']}")
                print(f"Mismatches   : {result['Mismatches']}")
            except ValueError as e:
                print(f"Error: {e}")


        elif choice == "9":
            print("Exiting program...")
            break

        else:
            print("Invalid option. Please enter a valid number from 1 to 9.")
            
if  __name__ == "__main__":
    main()

                    



