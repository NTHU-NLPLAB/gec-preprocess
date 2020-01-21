# gec-preprocess: a toolkit for preprocessing GEC data
`gecpt` is a toolkit for preprocessing grammatical error correction data (e.g., [FCE](https://ilexir.co.uk/datasets/index.html), [NUCLE](https://www.comp.nus.edu.sg/~nlp/conll14st.html), [Lang-8](https://sites.google.com/site/naistlang8corpora/), [WikEd](http://romang.home.amu.edu.pl/wiked/wiked.html), [JFLEG](https://github.com/keisks/jfleg), [EFCAMDAT](https://corpus.mml.cam.ac.uk/efcamdat2/)).
You can use it to convert learner corpora from one format to the other (e.g., xml-like to m2, m2 to [diff+](#diff+-format), diff to parallel, etc).

## Install gec-preprocess

```bash
pip install https://github.com/NTHU-NLPLAB/gec-preprocess/archive/master.zip
```

## Usage

1. Convert FCE xml files to diff+
```bash
cat fce.xml | python -m gecpt.format.fce_to_diff
```

```python
from gecpt.format import fce_to_diff

diff_text = fce_to_diff('The show is going to be in <NS type="MD"><c>the</c></NS> Central Exhibition Hall')
print(diff_text)
```

2. Convert diff+ format to parallel
```console
cat diff.txt | python diff_to_parallel.py
```

or use it in python

```python
from gecpt import diff_to_parallel

original, corrected = diff_to_parallel("We can discuss [-about-](U:PREP) the issue.")
print(original, '->', corrected)
```

## Diff+ format
`diff+` is a format for representing possibly erroneous sentences with corrective edits.
The format originated from the commonly used [wdiff](https://www.gnu.org/software/wdiff/).