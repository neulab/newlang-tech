# Building Machine Translation for New Languages

Machine Translation (MT) is the task of translating (written) text between languages.
It is useful to allow communication between people who don't speak a common language

## Obtaining Data

In general to train a machine translation system between two languages A and B, one needs to have *parallel data* for those two languages, that is, a corpus of sentences in language A and the corresponding translation for them in language B.

### Using Existing Corpora

Fortunately, there already exist parallel corpora for many language pairs 

* [OPUS](https://opus.nlpl.eu/): A collection of translated texts collected from the internet, already preprocessed. It covers over 100 languages, with different corpora for each language pair.

### Mining Data from the Internet

However, sometimes, no previous parallel corpora for the languages we are interested in exists. In such cases, if the languages are present on the internet, the cheapest approach is to procedurally *mine* a parallel corpus from the internet by using alignment algorithms that align sentences from the web pages with the same content in different languages.

* [CCMatrix](https://arxiv.org/pdf/1911.04944.pdf): Introduce a procedure for mining sentences from the internet by using large crawls over the whole internet (with more than 30 billion sentences) and using state-of-the-art alignment techniques. They release an extracted corpus covering 576 language pairs, but it is possible to reuse their procedure to extract parallel corpora for new languages.

One important consideration to have is that mined corpora might be *noisy* due to the quality of sentences on the internet and problems with the alignment algorithms, which can lead to *sub-par* machine translations models.

### Collecting Your Own Data

You can also create your own parallel corpora if no (good) corpora exist and your mining from the internet is not an option.

TODO: Procedure for doing this

## Training a Machine Translation System

After collecting the data, there are many available frameworks for training your models

* [FairSeq](https://github.com/pytorch/fairseq) is a sequence modelling toolkit based on PyTorch that supports machine translation. The advantages are that it's written in Python (making it relatively easy to learn), it's well tested, and it's fast. However, it doesn't include a ready-to-use solution for the deployment of trained models.
* [MarianNMT](https://marian-nmt.github.io/) is a machine translation framework written in C++ with minimal dependencies. Its advantages are that it's *fast* and it comes with ready-to-use use deployment solutions. However, being written in C++ might make it harder to get started with it.

Overall we recommend starting with FairSeq due to its relative ease of use. A good starting point is the [scripts for training small models in WMT14](https://github.com/pytorch/fairseq/tree/main/examples/translation). Another possible approach is finetuning a multilingual model pretrained on many languages, such as the [M2M-100 model](https://github.com/pytorch/fairseq/tree/main/examples/m2m_100), especially if such languages are similar to the languages we are targeting.

## Evaluating a Machine Translation System

Evaluating a machine translation system is very much an open problem and an active research area. The best way to evaluate such systems is to do a **human evaluation** since it's the most reliable way to compare how the translations provided by the model compare to human references. For example, one might hire annotators that speak both languages that our system targets from freelancing platforms such as [Upwork](https://www.upwork.com/) and asking them to rate a system, as well as the human reference translations. 

However, human evaluation is expensive, making it hard to use as evaluation for iterating over models. Fortunately, automatic metrics exist. While they aren't as reliable as human evaluation, they are cheap to compute and generally allow us to tell if a model is improving. Some commonly used metrics are:

* **BLEU**: Based on comparing lexical features of the reference and system translation, BLEU has been the *de-facto* standard for evaluating MT systems. While many concerns have been raised recently about its correlation with human judgements, it's still widely reported when evaluating MT systems, since it is fast to compute and well-studied. The most commonly used implementation is [SacreBLEU](https://github.com/mjpost/sacrebleu).
* **COMET**: Based on recent advances in pretrained cross-lingual language models, COMET is a neural evaluation metric that was trained to predict human quality assessments and it has been shown to correlate better human judgements than lexical-based metrics such as BLEU, therefore being a better indicator of a system's performance. However, unlike lexical metrics, it only supports a pre-defined set of languages and can be more expensive to compute than BLEU. The official implementation with pretrained models can be found [here](https://github.com/Unbabel/COMET).

The recommended way to evaluate a system is then to use an *automatic metric* to provide cheap evaluations of a system while iterating over approaches and, when confident that the model is good, performing a final *human evaluation* to have a more accurate assessment of its quality.
