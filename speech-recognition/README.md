# Building Speech Recognition for New Languages

Speech recognition is a task to transcribe speech into text. It is useful if you want to build a speech interface.

## Collecting Data

The availability of training set typically depends on your target language. We consider 4-levels based on the ranks of speaker population..

### English and Mandarin (> 10k hours)

For English and Mandarin, it is easy to obtain more than 1k hours training set, and sometimes even more than 10k hours.

For example, some recent large corpus are:

- English: [GigaSpeech](https://github.com/SpeechColab/GigaSpeech)
- Mandarin: [WenetSpeech](https://wenet-e2e.github.io/WenetSpeech/)


### Top-50 Language (> 100 hours)

The Top-50 Languages usually have more than 100 hours training set, some common websites to collect speech data are 

- [Common Voice](https://commonvoice.mozilla.org/en/datasets): has more than 50 languages
- [OpenSLR](https://openslr.org/): has many good quality speech data
- [LDC](https://www.ldc.upenn.edu/): may require licence to download


### Top 500 Language (> 1 hour)

From here, it is usually within the realm of low resource languages. It might be hard to obtain speech transcribed dataset, but there are some options. For example,

- [CMU Wilderness Corpus](https://github.com/festvox/datasets-CMU_Wilderness): This is a very broad corpus with 699 languages, but not all languages are well-aligned.


### Other Language (< 1 hour)

For languages that are not included in the top-500 languages, you should consider creating dataset yourself. See the next section.


## Creating Data

TODO (xinjianl): explain how to create dataset from scratch

## Training a Speech Recognition

### Setup a ESPnet recipe

If you are not familiar with ESPnet, you should watch this [Youtube tutorial](https://www.youtube.com/watch?v=2mRz3wH1vd0)


### Training model

TODO: This should be filled in.



## Evaluating Speech Recognition Accuracy

TODO: Evaluating synthesizer accuracy info.

## Improving Your System

TODO: Once the system is created, there are several ways to improve it.