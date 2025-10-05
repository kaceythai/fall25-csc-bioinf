#!/bin/bash

# This line ensures that the script will exit immediately if any command fails.
# It's a good practice for automation to prevent unexpected behavior.
set -euxo pipefail

# --- N50 Calculation Function ---
# This function calculates the N50 score from a FASTA file.
# N50 is a common metric in genomics for assessing assembly quality.
# It reads all sequence lengths, sorts them, and finds the length of the
# contig at the halfway point of the total assembly size.
n50() {
    awk 'BEGIN{RS=">"; FS="\n"} NR>1{seqlen[NR-1]=length($2)} \
         END{asort(seqlen); totalsum=0; for(i in seqlen) totalsum+=seqlen[i]; \
         partsum=0; for(i in seqlen){partsum+=seqlen[i]; \
         if(partsum>=totalsum/2){print seqlen[i]; break}}}' $1
}

# --- Evaluation Function ---
# This function runs the assembler for a given dataset and language (python/codon),
# times its execution, and prints the results.
run_eval() {
    local dataset=$1
    local lang=$2
    local code_dir="week1/code"
    local data_dir="week1/data/${dataset}"
    
    # Choose the correct command based on the language
    if [ "$lang" == "python" ]; then
        CMD="python3 $code_dir/main.py $data_dir"
    else
        # Use the 'codon run -release' command for optimized timing
        CMD="$HOME/.codon/bin/codon run -release $code_dir/main.py $data_dir"
    fi
    
    # Execute and time the command.
    # The `time -p` command prints timing info to stderr, which we capture.
    runtime=$( (time -p $CMD) 2>&1 | awk '/^real/ {print $2}' )
    
    # Calculate N50 from the generated output file
    n50_score=$(n50 "$data_dir/contig.fasta")
    
    # Print a formatted row for our results table
    printf "%-10s\t%-10s\t%-10s\t%-10s\n" "$dataset" "$lang" "$runtime" "$n50_score"
}

# --- Main Script Execution ---

echo "Starting evaluation on Sunday, October 5, 2025 from Victoria, BC."
echo ""

# Print the header for the results table
printf "%-10s\t%-10s\t%-10s\t%-10s\n" "Dataset" "Language" "Runtime(s)" "N50"
echo "-----------------------------------------------------------------"

# Loop through each 'data' folder and run the evaluation for both Python and Codon
for data_dir in week1/data/data*; do
    dataset=$(basename "$data_dir")
    run_eval "$dataset" "python"
    run_eval "$dataset" "codon"
done
