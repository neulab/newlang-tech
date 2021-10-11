# Building Named Entity Recognition for New Languages

Named entity recognition (NER) is the task of recognizing named entities such as people, places, and organizations. It is useful if you want to analyze text in many cases.

## Collecting Data

There are some sources for labeled NER data that can be used to train systems. 

* [WikiAnn Corpus](https://huggingface.co/datasets/wikiann): A broad corpus automatically created from data from Wikipedia.
* [MasakhaNER Corpus](https://github.com/masakhane-io/masakhane-ner): A corpus of NER data from African languages.

## Creating Data

You can also create data yourself if it doesn't exist.

* Start by collecting unlabelled texts from popular domains like News articles or Wikipedia. If unlabelled texts do not exist, you can translate some sentences. 
* Start with few sets of entities especially the popular ones like Personal names (PER), organization (ORG), and location (LOC) or geopolitical entities (GPE). With few sets of entities, one can easily ensure high quality annotation since fine-grained entities and numerous entities can affect the quality of the overall process especially for non-expert annotators. 
* Familiarize yourself with annotation guides that have been used to develop popular NER datasets like the Message Understanding Conference [(MUC-6)guideline](https://cs.nyu.edu/faculty/grishman/NEtask20.book_1.html) and [LDC guideline](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-entities-guidelines-v6.6.pdf)
* 
TODO: A good procedure to do this should be filled in.

## Training a Named Entity Recognition System

TODO: This should be filled in.

## Evaluating Entity Recognition Accuracy

TODO: Evaluating NER accuracy info.

## Improving on Your System

TODO: Once you have a system, how can you improve it.
