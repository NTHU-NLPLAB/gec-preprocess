# gec-preprocess: a toolkit for preprocessing GEC data
`gept` is a toolkit for preprocessing grammatical error correction data (e.g., [FCE](https://ilexir.co.uk/datasets/index.html), [NUCLE](https://www.comp.nus.edu.sg/~nlp/conll14st.html), [Lang-8](https://sites.google.com/site/naistlang8corpora/), [WikEd](http://romang.home.amu.edu.pl/wiked/wiked.html), [JFLEG](https://github.com/keisks/jfleg), [EFCAMDAT](https://corpus.mml.cam.ac.uk/efcamdat2/)).

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
