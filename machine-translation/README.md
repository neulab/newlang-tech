# Building Machine Translation for New Languages

Machine Translation (MT) is the task of translating (written) text between languages.
It is useful to allow communication between people who don't speak a common language

# Obtaining Data

In general to train a machine translation system between two languages A and B, one needs to have *parallel data* for those two languages, that is, a corpus of sentences in language A and the corresponding translation for in language B.

**TODO**: Section for unsupervised/transfer from other pairs

## Using Existing Corpora

Fortunatly there are currenly parallel corpora for many language pairs 

* [OPUS](https://opus.nlpl.eu/): A collection of translated texts collected from the internet, already preprocessed. It covers over 100 languages, with different corpora for each language pair.

## Creating your Own Corpora

You can also create data yourself if it doesn't exist.

### Mining from the Internet

TODO: Elaborate more on this

* [CCMatrix](https://arxiv.org/pdf/1911.04944.pdf): Introduce a procedure for mining sentences from the internet

### Collecting your own data

You can also create your own parallel corpora if no (good) corpora exist and you mining from the internet is not an option

TODO: You can also create data yourself if it doesn't exist.

# Training a Machine Translation System

After collecting, there are many available frameworks for training your own models

* [MarianNMT](https://marian-nmt.github.io/)
* [FairSeq](https://github.com/pytorch/fairseq)

TODO: Elaborate on advantages between the frameworks

# Evaluating a Machine Translation System

TODO: Evaluating NER accuracy info.

# Improving on Your System

TODO: Once you have a system, how can you improve it.