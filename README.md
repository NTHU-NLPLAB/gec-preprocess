# gec-preprocess: a toolkit for preprocessing GEC data
`gecpt` is a toolkit for preprocessing grammatical error correction data (e.g., [FCE](https://ilexir.co.uk/datasets/index.html), [NUCLE](https://www.comp.nus.edu.sg/~nlp/conll14st.html), [Lang-8](https://sites.google.com/site/naistlang8corpora/), [WikEd](http://romang.home.amu.edu.pl/wiked/wiked.html), [JFLEG](https://github.com/keisks/jfleg), [EFCAMDAT](https://corpus.mml.cam.ac.uk/efcamdat2/)).
You can use it to convert learner corpora from one format to the other (e.g., xml-like to m2, m2 to [diff+](#diff+-format), diff to parallel, etc).

## Install gec-preprocess

```bash
pip install https://github.com/NTHU-NLPLAB/gec-preprocess/archive/master.zip
```

## Usage

### Use it in terminal

1. Convert FCE xml files to diff+
```bash
cat fce.xml | python -m gecpt.format.convert_fce
```

2. Convert diff+ format to parallel
```bash
cat diff.txt | python -m gecpt.format.diff_to_parallel
```

### Use it in python

1. Convert FCE xml files to diff+
```python
from gecpt.format import convert_fce

diff_text = convert_fce('The show is going to be in <NS type="MD"><c>the</c></NS> Central Exhibition Hall', to='diff')
print(diff_text)
# The show is going to be in {+the+}(MD) Central Exhibition Hall
```

2. Convert diff+ format to parallel
```python
from gecpt.format import diff_to_parallel

original, corrected = diff_to_parallel("We can discuss [-about-](U:PREP) the issue.")
print(original, '->', corrected)
# We can discuss about the issue. -> We can discuss the issue.
```

3. Convert m2 format to diff+
```python
from gecpt.format import iter_m2_file, parse_m2_token, convert_m2


def m2_to_diff(m2_contents):
    wdiff_sents = []
    for sent, *edits in iter_m2_file(m2_contents):
        edits_tuples = [parse_m2_token(edit) for edit in edits]
        wdiff_sents.append(convert_m2(sent[2:], edits_tuples))
    return wdiff_sents


m2_contents = [
  'S But , if you want I look for a job from you .',
  'A 5 5|||M:PUNCT|||,|||REQUIRED|||-NONE-|||0',
  'A 6 6|||M:VERB:TENSE|||will|||REQUIRED|||-NONE-|||0',
  'A 10 11|||R:PREP|||for|||REQUIRED|||-NONE-|||0',
  '',  # extra new line is necessary.
]

print(m2_to_diff(m2_contents)[0])
# 'But , if you want {+,+}(M:PUNCT) I {+will+}(M:VERB:TENSE) look for a job [-from-]{+for+}(R:PREP) you .'
```

## Diff+ format
`diff+` is a format for representing possibly erroneous sentences with corrective edits.
The format originated from the commonly used [wdiff](https://www.gnu.org/software/wdiff/).
