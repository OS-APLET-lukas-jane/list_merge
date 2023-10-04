# List Merge

## Description

`list_merge` is a Python tool designed to merge wordlists based on a predefined password policy. It ensures that the merged list only contains passwords that meet specific criteria, such as the inclusion of uppercase and lowercase letters, numbers, and special characters.

For example, Rockyou and SecLists result in a 48mb wordlist compared to roughly 900mb.

## Features

- Merges multiple wordlists into a single list
- Filters out passwords that don't meet the local Windows policy
- Supports both single file and directory-based wordlist merging

## Installation

```
#Pull the repo
git clone https://github.com/0xdreadnaught/list_merge.git

#Install TQDM for progress bars
pip3 install tqdm
```

## Usage

### Basic Usage

```
python3 list_merge.py <source_wordlist> <destination_wordlist>
```

### Ingest Mode

Recursively process all `.txt` files in a directory:

```
python list_merge.py --ingest <source_directory> <destination_wordlist>
```

