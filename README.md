# gec-preprocess: a toolkit for preprocessing GEC data


## Install gec-preprocess

```bash
pip install https://github.com/NTHU-NLPLAB/gec-preprocess/archive/master.zip
```


## Usage

```python
from gecpt import diff_to_parallel

original, corrected = diff_to_parallel("We can discuss [-about-](U:PREP) the issue.")
print(original, '->', corrected)
```
