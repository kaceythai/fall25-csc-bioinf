#!/bin/bash
# BioProject Analysis Log
# Student: Kacey Friesen
# Date: Dec 4, 2025

# 1: Structural Alignment (MUMmer 3.1)
# Navigate to data directory
# Comparing Copenhageni (Ref) vs Lai (Query)
# --maxmatch is used to find all matches regardless of uniqueness, critical for finding inversions flanked by repeats.

nucmer --maxmatch -c 100 -p ../results/alignment/comparison ../data/copen.fna ../data/lai.fna

# Generate the Dot Plot
# --large is used to optimize the layout for whole-genome viewing
mummerplot --png --large --layout --title "Lai vs Copenhageni" -p ../results/figures/my_plot ../results/alignment/comparison.delta

# 2: Virulence Factor Screening (Grep)
# Counting total "immunoglobulin-like" proteins to see broad differences
grep -c "immunoglobulin-like" ../data/copen_protein.faa > ../results/virulence/copen_lig_count.txt
grep -c "immunoglobulin-like" ../data/lai_protein.faa > ../results/virulence/lai_lig_count.txt

# Checking for specific LigA presence in Lai (The Discrepancy Check)
# This command extracts the header and first few lines of sequence
grep -A 10 "LigA" ../data/lai_protein.faa > ../results/virulence/lai_ligA_hits.txt