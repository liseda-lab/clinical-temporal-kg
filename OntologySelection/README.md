# Ontology Selection Based on Coverage

The process fo ontology selection varies much depending on the featues in analysis.
For our particular case, we are dealing with free text variables regarding diagnosis, as such and to ensure domain relevance, we pre select a set of ontologies and analyse their coverage on the diagnosis set to choose the most appropriate one.

While different ontology selection methods exist, for this method, we choose the NCBO's BioPortal Recommender platform due to its large biomedical repository.

Disclaimer: The results presented our manuscript were obtained using the versions and NCBO resorses valid in 2022. As such, coverages may change abd run times and server related issues may appear. However we are confident the rankings we showcase will be accurate.


## Requirements for selection:

1. Acess to NCBO recoomender. (https://bioportal.bioontology.org/recommender)
2. Have a valid NCBO API key.
3. Pre select a set of ontologies.


## Runing the script to get the coverages:

1. Acess the script 'RecommenderCoverage.py'.
```python
    cd OntologySelection
    open formatAlignment.py
```
2. Change the paths to the targeted files.
3. Put your API key.
4. Run the script.
```python
    python3 formatAlignment.py
```

