# Building Speech Recognition for New Languages

Speech recognition is a task to transcribe speech into text. It is useful if you want to build a speech interface.

## 1. Collecting Data

The availability of training set typically depends on your target language. 

We can classify all languages into 4 groups depending on the amount of training set, the group is highly related to the each language's speaker population and economic factors.

### 1.1. English and Mandarin (> 10k hours)

For English and Mandarin, it is easy to obtain more than 1k hours training set, and sometimes even more than 10k hours.

For example, some recent large corpus are:

- English: [GigaSpeech](https://github.com/SpeechColab/GigaSpeech)
- Mandarin: [WenetSpeech](https://wenet-e2e.github.io/WenetSpeech/)


### 1.2. Top-50 Language (> 100 hours)

The Top-50 Languages usually have more than 100 hours training set, some common websites to collect speech data are 

- [Common Voice](https://commonvoice.mozilla.org/en/datasets): has more than 50 languages
- [OpenSLR](https://openslr.org/): has many good quality speech data
- [LDC](https://www.ldc.upenn.edu/): may require licence to download


### 1.3. Top 500 Language (> 1 hour)

From here, it is usually within the realm of low resource languages. It might be hard to obtain speech transcribed dataset, but there are some options. For example,

- [CMU Wilderness Corpus](https://github.com/festvox/datasets-CMU_Wilderness): This is a very broad corpus with 699 languages, but not all languages are well-aligned.


### 1.4. Other Language (< 1 hour)

For languages that are not included in the top-500 languages, you should consider creating dataset yourself. See the next section.


## 2. Creating Data

There are two potential ways to collect speech traning set. We need to prepare either the text data or audio data to start with. 

### 2.1 Creating data from texts

To create a datset from texts, We first need to prepare a text file containing utterances. Ideally, the utterances should be related to the domain you want to recognize. To collect the data, we need to record audios for each utterance.

There are two ways to do the recording:

1. We ask the speaker to read out every utterance in the text file without stopping. Between every utterance, the speaker should be silent and wait 2~3 seconds.
2. We can also record each utterance one by one, each utterance should be explicitly stored in different files.

The 1st approach is much easier and would save time for the speaker, but it requires more efforts to do the postprocessing because we need to segment the recordings to the utterance-level. As we ask the speaker to be silent between utterances, the silence part in the audio should be easily detected by some voice activity detection tools such as [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)

See more recording tips in the [Speech Synthesis](speech-synthesis/).

### 2.2 Creating data from audios

We can also create dataset from audios by providing transcriptions to each utterance. If the audio contains multiple utterances, we first need to do the segmentation. Similarly, this segmentation can be done using voice activity detection tools such as [py-webrtcvad](https://github.com/wiseman/py-webrtcvad) or other speaker diarization tools.

For each short audio clip, we should ask the annotator to transcribe its contents into text form. If the audio is too noisy or not clear, it should be discarded.


## 3. Training a Speech Recognition

In this section, we describe how to train a speech recognition model using the [ESPnet framework](https://github.com/espnet/espnet)

If you are not familiar with ESPnet, you should watch this [Youtube tutorial](https://www.youtube.com/watch?v=2mRz3wH1vd0)


### 3.1. Setup a ESPnet recipe

TODO


### 3.2. Training model

TODO: This should be filled in.


## 4. Evaluating Speech Recognition Accuracy

TODO: Evaluating synthesizer accuracy info.

## 5. Improving Your System

TODO: Once the system is created, there are several ways to improve it.

## 6. Reference

