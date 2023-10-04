import sys
import os
import re
import argparse
from tqdm import tqdm


def check_password_policy(password):
    """
    Check if the given password meets the local Windows policy.

    Parameters:
        password (str): The password string to check.

    Returns:
        bool: True if the password meets the policy, False otherwise.
    """
    if (
        re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        and not re.search(r" ", password)
    ):
        return True
    return False


def write_to_dest_file(dest_words, dest_file):
    """
    Write the destination words to a file and reload them.

    Parameters:
        dest_words (set): The set of destination words.
        dest_file (str): The path to the destination file.
    """
    with open(dest_file, "w", encoding="latin-1") as dest_f:
        for word in dest_words:
            dest_f.write(f"{word}\n")
    # Reload the destination wordlist
    with open(dest_file, "r", encoding="latin-1") as f:
        dest_words.clear()
        dest_words.update(line.strip() for line in f)


def process_file(source_file, dest_words):
    """
    Process a source file and update the destination words.

    Parameters:
        source_file (str): The path to the source file.
        dest_words (set): The set of destination words.
    """
    added_count = 0
    try:
        with open(source_file, "rb") as source_f:
            lines = source_f.readlines()
            for line in tqdm(lines, desc=f"Processing {source_file}"):
                word = line.decode("latin-1").strip()
                if word not in dest_words:
                    if check_password_policy(word):
                        dest_words.add(word)
                        added_count += 1
    except Exception as e:
        print(f"Error processing {source_file}: {e}")
    print(f"Added {added_count} passwords.")


def main():
    """
    Main function to handle command-line arguments and initiate processing.
    """
    parser = argparse.ArgumentParser(
        description="Merge wordlists with password policy checks."
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest mode to process all txt files in a directory",
    )
    parser.add_argument("source", help="Source wordlist or directory")
    parser.add_argument("destination", help="Destination wordlist")

    args = parser.parse_args()

    source = args.source
    dest_file = args.destination

    dest_words = set()

    if os.path.exists(dest_file):
        with open(dest_file, "r", encoding="latin-1") as f:
            dest_words = set(line.strip() for line in f)
    if args.ingest:
        for root, dirs, files in os.walk(source):
            for file in files:
                if file.endswith(".txt"):
                    process_file(os.path.join(root, file), dest_words)
                    write_to_dest_file(dest_words, dest_file)
    else:
        process_file(source, dest_words)
        write_to_dest_file(dest_words, dest_file)


if __name__ == "__main__":
    main()
