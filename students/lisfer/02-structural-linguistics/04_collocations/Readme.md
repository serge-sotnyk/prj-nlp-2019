# Collocations

## Installation

```bash
virtualenv venv -p python3
source ./venv/bin/activate
pip install spacy
python -m spacy download en_core_web_md
```

## Run Program

Needs file `SentiWordNet_3.0.0.txt` to be present in current catalog. Or it may be changed in the code (line 7, variable `FILE_SENTI`)

```
./venv/bin/python main.py <income_file>
```

## Results

```python
announce [
    ('recently', 15), ('officially', 11), ('publicly', 8), ('proudly', 4), ('early', 4), ('shortly', 4), ('openly', 3), ('previously', 3), ('quickly', 3), ('newly', 3)]
chat [
    ('directly', 1), ('coincidentally', 1)]
claim [
    ('falsely', 65), ('previously', 9), ('repeatedly', 8), ('recently', 4), ('initially', 3), ('actually', 3), ('absurdly', 3), ('credibly', 3), ('publicly', 3), ('laughably', 3)]
communicate [
    ('effectively', 3), ('directly', 3), ('freely', 1), ('really', 1), ('apparently', 1), ('loudly', 1), ('hopefully', 1), ('daily', 1), ('actually', 1), ('regularly', 1)]
convey [
    ('accurately', 3), ('usually', 2), ('fully', 2), ('sharply', 1), ('clearly', 1), ('only', 1), ('privately', 1), ('strongly', 1)]
explain [
    ('clearly', 11), ('fully', 10), ('patiently', 6), ('probably', 6), ('certainly', 5), ('really', 5), ('easily', 4), ('exactly', 4), ('recently', 4), ('necessarily', 2)]
express [
    ('repeatedly', 6), ('actually', 3), ('privately', 3), ('freely', 3), ('openly', 2), ('publicly', 2), ('starkly', 2), ('finally', 2), ('only', 2), ('verbally', 1)]
inform [
    ('fully', 3), ('personally', 3), ('accurately', 2), ('actually', 2), ('snidely', 1), ('merely', 1), ('quietly', 1), ('factly', 1), ('truthfully', 1), ('curtly', 1)]
instruct [
    ('obviously', 1), ('endlessly', 1), ('erroneously', 1), ('naturally', 1), ('reportedly', 1), ('subliminally', 1), ('finally', 1), ('explicitly', 1)]
notify [
    ('properly', 1)]
point [
    ('rightly', 14), ('simply', 8), ('repeatedly', 7), ('recently', 6), ('only', 5), ('correctly', 5), ('actually', 4), ('quickly', 4), ('finally', 3), ('specifically', 3)]
recite [
    ('simply', 3), ('robotically', 1), ('rapidly', 1), ('properly', 1)]
reckon [
    ('differently', 1)]
refer [
    ('apparently', 6), ('specifically', 6), ('repeatedly', 6), ('clearly', 4), ('commonly', 4), ('previously', 3), ('usually', 3), ('obliquely', 3), ('generally', 2), ('incorrectly', 2)]
report [
    ('recently', 31), ('widely', 17), ('previously', 13), ('breathlessly', 10), ('finally', 9), ('directly', 7), ('simply', 5), ('separately', 5), ('only', 4), ('honestly', 4)]
say [
    ('recently', 77), ('actually', 74), ('repeatedly', 55), ('simply', 46), ('explicitly', 38), ('publicly', 36), ('basically', 35), ('really', 31), ('only', 25), ('clearly', 23)]
speak [
    ('directly', 32), ('publicly', 15), ('only', 12), ('fiercely', 12), ('briefly', 9), ('generally', 8), ('finally', 8), ('openly', 8), ('politically', 7), ('loudly', 7)]
talk [
    ('directly', 14), ('really', 12), ('only', 9), ('openly', 7), ('actually', 7), ('publicly', 6), ('repeatedly', 6), ('personally', 5), ('clearly', 5), ('constantly', 5)]
tell [
    ('recently', 25), ('reportedly', 14), ('privately', 11), ('specifically', 9), ('finally', 9), ('only', 9), ('basically', 9), ('actually', 8), ('really', 8), ('simply', 8)]
utter [
    ('actually', 1), ('casually', 1), ('only', 1)]
voice [
    ('openly', 2), ('surprisingly', 1), ('recently', 1), ('frequently', 1), ('infamously', 1), ('consistently', 1), ('reportedly', 1), ('rarely', 1), ('explicitly', 1), ('repeatedly', 1)]
whisper [
    ('usually', 1), ('playfully', 1), ('reportedly', 1)]

```