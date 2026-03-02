

import os
import re
from collections import Counter
from prettytable import PrettyTable

# Provided pattern (bytes)
wPatt = re.compile(b"[a-zA-Z]{5,15}")

def scan_memdump(file_path, chunk_size=4 * 1024 * 1024, carry_size=50):
    counts = Counter()
    carry = b""

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            data = carry + chunk

            # Count matches
            for m in wPatt.findall(data):
                # normalize to lowercase for "unique" (OPTIONAL but usually expected)
                counts[m.lower()] += 1

            # keep a small overlap so words split across chunks are still found
            carry = data[-carry_size:]

    return counts

def main():
    mem_path = input("Enter path to mem.raw: ").strip().strip('"').strip("'")

    if not os.path.isfile(mem_path):
        print("File not found. Check the path and try again.")
        return

    counts = scan_memdump(mem_path)

    # Build PrettyTable
    table = PrettyTable()
    table.field_names = ["String", "Occurrences"]

    # Sort by most common
    for word_bytes, freq in counts.most_common():
        word = word_bytes.decode("utf-8", errors="ignore")
        if word:  # just in case decode produces empty
            table.add_row([word, freq])

    print(table)

    
    out_file = "string_frequency_report.txt"
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(str(table))

    print(f"\nSaved table to: {out_file}")

if __name__ == "__main__":
    main()
