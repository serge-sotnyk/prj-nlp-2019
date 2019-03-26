# Viral News

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

## Results:

Marked as personal - if a person was found in the title

Marked as comparison - if found at least one token with an attribute `Degree` in (`sup`, `comp`)

Marked as sentiment. We take all senses of the word with same POS. And if avg(postive + negative values) > 0.5, we mark it as word with a sentiment.   


```
Rated as personal: 1442 from 5000 == 28.84%
Rated as comparison: 234 from 5000 == 4.68%
Rated as sentiment: 672 from 5000 == 13.44%
```