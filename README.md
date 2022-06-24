# Sommarioni data extraction


The aim of this project is to extract entities (people, instutions) and their relationships from the 1808 Venetian Sommarioni, the registry accompanying the 1808 Napoleonian cadaster.

At the moment, all 23'000 entries have been classified in categories based on their content and extraction requirements. 

This repository is the result of a bachelor semester project at the DHLAB EPFL in the spring 2022.

## Folder structure

Folders:
- `scripts/`: this is where you'll spend most of your time, writing scripts to download data, train models, create graphs etc. Each main step of the project has its own numbered subfolder, for example:
    + `s0_list_of_terms/`: text-cleaning, replacement of "suddetto", duplicated entries, etc.
    + `s1_classification/`: entries classification: single person, family, church, municipality of Venice, etc.
    + `s2_extraction/`:  extraction of people and their links
- `data/`:
- `src/classes.py`: defines the data-structure for people


