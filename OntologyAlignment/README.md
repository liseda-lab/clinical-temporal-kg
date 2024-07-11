# Stepts to extend the TKG with ontology alignment

This folder contains the necessary information to perform ontology alignment in the way intended by our method.
To ensure that, we provide the necessary direction to produce the alignment files and our own in case of an issue.

## To perform Ontology Alignment we use the AML tool.

The tool is available at https://github.com/AgreementMakerLight/AML-Project.

Please follow the introductions for intalation and use provided by the source repository.

## Requirements:

- Download the fowing ontologies: ICD9CM, DRON, LOINC and NCIT. All are available at: https://bioportal.bioontology.org.
- Have AML installed.

## Setps to use AML for our implementation:

1. Open the file tab and select 'Open Ontologies'.
2. Load the Source ontology.
3. Load the Target ontology.
4. Open the Match tab and run the 'Automatic Matcher'.
5. Download the alignment (rdf format).

## Steps to prepare the alignment files to extend the KG:

1. Place them in the OntologyAlignment directory ./OntologyAlignment .
2. Run the script formatAlignment.py.
```python
    cd /AlignmentFile
    python3 formatAlignment.py
```
3. The final results are on the triples files directory formated as both tsv and turtle.
```python
    cd /TriplesFiles
```
