# Building Named Entity Recognition for New Languages

Named entity recognition (NER) is the task of recognizing named entities such as people, places, and organizations. It is useful if you want to analyze text in many cases.

## Collecting Data

There are some sources for labeled NER data that can be used to train systems. 

* [WikiAnn Corpus](https://huggingface.co/datasets/wikiann): A broad corpus automatically created from data from Wikipedia.
* [MasakhaNER Corpus](https://github.com/masakhane-io/masakhane-ner): A corpus of NER data from African languages.

## Creating Data

You can also create data yourself if it doesn't exist.

* Start by collecting unlabelled texts from popular domains like News articles or Wikipedia. If unlabelled texts do not exist, you can translate some sentences. 
* Start with few sets of entities especially the popular ones like Personal names (PER), organization (ORG), location (LOC) and/or geopolitical entities (GPE). With few sets of entities, one can easily ensure high quality annotation since fine-grained entities and numerous entities can affect the quality of the overall process especially for non-expert annotators. 
* Familiarize yourself with annotation guides that have been used to develop popular NER datasets like the Message Understanding Conference [(MUC-6) guideline](https://cs.nyu.edu/faculty/grishman/NEtask20.book_1.html) and [LDC guideline](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-entities-guidelines-v6.6.pdf)
* Look for an easy to use annotation tool like [ELISA](https://aclanthology.org/P18-4001/), [brat](https://brat.nlplab.org/index.html), [Prodigy](https://prodi.gy/), [LightTag](https://www.lighttag.io/), [ioAnnotator](https://ioannotator.com/),  etc. Some provide the tool free for academic use.
* Create your own annotation guide with examples in the language or domain of interest. Preferrably, with examples from the annotation tool.
* (Optionally) Create a pre-recorded video on how to use the tool especially if you are working with non-expert annotators. 
* Recruit odd number of annotators if possible, so that their inter-agreement score can be compared and you can make use of majority vote. Set your required inter-agreement score to be high (e.g at least 0.95) especially for the trial examples. 
* Ask your annotators to start with a few set of sentences e.g 10 or 100, and evaluate their inter-agreement scores. Some tools provide this for you. 
* When annotation is done, prepare your final dataset in CoNLL format i.e <word>[space]<tag>, and sentences are demarcated with an additional empty line. An example is [here](https://github.com/masakhane-io/masakhane-ner/blob/main/data/pcm/dev.txt). The recommended tagging scheme is BIO or IOB2 where "B-" signifies the beginning of an entity, "I-" signifies the inside of an entity and "O"- outside of an entity or no entity. Other tagging schemes are IOBES and IOB1.  

## Training a Named Entity Recognition System
  
There are several NER models that can be trained, the best approach is fine-tuning pre-trained language models (PLMs) like BERT. 

You can use the official token classification code from [HuggingFace Transformers](https://github.com/huggingface/transformers/tree/master/examples/pytorch/token-classification). Fine-tuned LM produces the state-of-the-art for this task. For other languages apart from English, you need to use multilingual variants of the pre-trained LM e.g mBERT, XLM-RoBERTa, InfoXLM, RemBERT, etc. 
  
Please, confirm if your script is covered in the vocabulary of the PLM. If not, one idea is to perform [vocabulary augmentation](https://aclanthology.org/2020.findings-emnlp.118/) with the new script tokens and further pre-train the PLM on unlabelled texts in the new language. 
  
## Evaluating Entity Recognition Accuracy
  
Accuracy of NER is measured using span F1-score i.e the model is penalized if it cannot sequentially detect a span of entities e.g "New York". Just correctly identifying "York" will result in incorrect prediction of both "New" and "York". 
  
You can use [seqeval](https://pypi.org/project/seqeval/) - a python implementation of the official [CoNLL Eval scripts](https://www.clips.uantwerpen.be/conll2000/chunking/conlleval.txt)
  
## Improving on Your System
  
Improving NER models is still a subject of research. The most effective method with pre-trained language model is based on transfer learning from different task, language or domain. 
  
* Domain/Language adaptive fine-tuning ([Gururangan et al., 2020](https://arxiv.org/abs/2004.10964)): involves first fine-tuning the masked language model on unlabelled texts in the target domain/language before fine-tuning on the available supervised learning dataset. For example, in the [MasakhaNER](https://arxiv.org/abs/2103.11811) paper, this helped to improve the performance by over 5% F1-score. 
 
* In the absence of training data or in zero-shot settings, one can train on a high resource language/domain that shares common target labels and domain. E.g Train on English CoNLL03 or WikiANN (in a similar language). 
