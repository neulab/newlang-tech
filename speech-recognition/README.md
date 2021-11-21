# Building Speech Recognition for New Languages

Speech recognition is a task to transcribe speech into text. It is useful if you want to build a speech interface.

## 1. Collecting Data

The availability of training set typically depends on your target language. 

We can classify all languages into 4 groups depending on the amount of training set. The group is highly related to each language's speaker population and economic factors.

### 1.1. English and Mandarin (> 10k hours)

For English and Mandarin, it is easy to obtain more than 1k hours training set, and sometimes even more than 10k hours.

For example, some recent large corpus are:

- English: [GigaSpeech](https://github.com/SpeechColab/GigaSpeech)
- Mandarin: [WenetSpeech](https://wenet-e2e.github.io/WenetSpeech/)


### 1.2. Top-50 Language (> 100 hours)

The Top-50 Languages usually have more than 100 hours training set. Some common websites to collect speech data are 

- [Common Voice](https://commonvoice.mozilla.org/en/datasets): has more than 50 languages
- [OpenSLR](https://openslr.org/): has much good quality speech data
- [LDC](https://www.ldc.upenn.edu/): may require a license to download


### 1.3. Top 500 Language (> 1 hour)

From here, it is usually within the realm of low-resource languages. It might be hard to obtain a speech transcribed dataset, but there are some options. For example,

- [CMU Wilderness Corpus](https://github.com/festvox/datasets-CMU_Wilderness): This is a very broad corpus with 699 languages, but not all languages are well-aligned.


### 1.4. Other Language (< 1 hour)

For languages that are not included in the top-500 languages, you should consider creating a dataset yourself. See the next section.


## 2. Creating Data

There are two potential ways to collect speech training set. We need to prepare either the text data or audio data to start with. 

### 2.1 Creating data from texts

To create a dataset from texts, We first need to prepare a text file containing utterances. Ideally, the utterances should be related to the domain you want to recognize. To collect the data, we need to record audios for each utterance.

There are two ways to do the recording:

1. We ask the speaker to read out every utterance in the text file without stopping. Between every utterance, the speaker should be silent and wait 2~3 seconds.
2. We can also record each utterance one by one. Each utterance should be explicitly stored in different files.

The 1st approach is much easier and would save time for the speaker, but it requires more effort to do the postprocessing because we need to segment the recordings to the utterance level. As we ask the speaker to be silent between utterances, the silence part in the audio should be easily detected by some voice activity detection tools such as [py-webrtcvad](https://github.com/wiseman/py-webrtcvad)

See more recording tips in the [Speech Synthesis](speech-synthesis/).

### 2.2 Creating data from audios

We can also create a dataset from audios by providing transcriptions to each utterance. If the audio contains multiple utterances, we first need to do the segmentation. Similarly, this segmentation can be done using voice activity detection tools such as [py-webrtcvad](https://github.com/wiseman/py-webrtcvad) or other speaker diarization tools.

For each short audio clip, we should ask the annotator to transcribe its contents into text form. If the audio is too noisy or not clear, it should be discarded.


## 3. Training a Speech Recognition

This section describes how to train a speech recognition model using the [ESPnet framework](https://github.com/espnet/espnet). This tutorial mainly focuses on ESPnet2 examples, which have a more pythonic solution with its feature extraction module.

We could find the installation of ESPnet at [ESPnet installation](https://espnet.github.io/espnet/installation.html).

You are encouraged to watch this [Youtube tutorial](https://www.youtube.com/watch?v=2mRz3wH1vd0) with step-by-step explanations.


### 3.1. Setup an ESPnet recipe

We first need to set up an experimental directory. This is rather easy with run `egs2/TEMPLATE/asr1/setup.sh`. The resulting directory would link the essential executable scripts and several example configurations for cluster users.

In the experimental directory, you should add `run.sh` to run the whole experiment. An example structure of `run.sh` could be:

```
#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

train_set="train"
valid_set="dev"
test_sets="test"

asr_config=conf/train_asr.yaml
lm_config=conf/train_lm.yaml
inference_config=conf/decode_asr.yaml

./asr.sh \
    --lang <YOUR_LANGUAGE_ID> \                     # Set it with your own language id, e.g., "en" for English
    --stage 1 \                                     # The start stage
    --stop_stage 100 \                              # The stop stage
    --ngpu 1 \                                      # Number of GPUs you will use for training
    --nbpe 100 \                                    # Number of word piece (bpe is for Byte-pair-encoding units) size
    --speed_perturb_factors "0.9 1.0 1.1" \         # Speed perturbation factor, usually "0.9 1.0 1.1" would be enough
    --asr_config "${asr_config}" \                  # ASR model configuration and training configuration
    --lm_config "${lm_config}" \                    # Language model configuration (we usually found language modeling helps the ASR)
    --inference_config "${inference_config}" \      # ASR inference configuration
    --train_set "${train_set}" \                    # Name of train set, will be located at `data/${train_set}`
    --valid_set "${valid_set}" \                    # Name of dev set, will be located at `data/${dev_set}`
    --test_sets "${test_sets}" \                    # Name of test set, will be located at `data/${test_set}`
    --lm_train_text "data/${train_set}/text" \      # Text file for training language model
    --bpe_train_text "data/${train_set}/text" "$@"  # Text for training word piece units
```

As shown in the example `run.sh`, the experiments will follow the order in `asr.sh`, which includes four sections: "data preparation", "training", "evaluation", "uploading". We will skip the last uploading section this time.

### 3.2 Data preparation

There are six stages in data preparation, but you only need to write extra codes for the first one. While for the following ones, you can set arguments at `run.sh` to proceed. For the first-time user, we recommend you to use default settings for those stages.

In the first stage, you need to prepare the `data` folder in your experimental directory. The folder should typically include `train`, `test`, and `dev` sets. For each set (a sub-folder in `data`), the following index files should be prepared:

```
wav.scp # the index mapping of wavID to wavfile path
utt2spk # the index mapping of uttID to spk ID
spk2utt # the index mapping of spkID to uttID
text    # the text information for each uttID
segments # (Optional) if each single wavfile contains many utterances, the segments show the mapping between wavID to uttID
         # otherwise, no need for this file
```
The formats of each file will be explained as follows:

#### 3.2.1 wav.scp

wav.scp can be as simple as:
```
WAV_ID1 /path/to/1.wav
WAV_ID2 /path/to/2.wav
...
```

The pipeline path is also supported. Please check this [example](https://github.com/espnet/espnet/blob/master/egs/commonvoice/asr1/local/data_prep.pl) for details.

#### 3.2.2 utt2spk and spk2utt

`utt2spk` will be formatted as:
```
UTT_ID1 SPK_ID1
UTT_ID2 SPK_ID1
UTT_ID3 SPK_ID2
...
```

After formating this file, you can easily generate `spk2utt` file by shell script `utils/spk2utt_to_utt2spk.pl`.

#### 3.2.3 text

`text` will be formatted as:
```
UTT_ID1 A B C
UTT_ID2 C D E
UTT_ID3 A B D
...
```

#### 3.2.3 segments

`segments` is optional. It should be presented if you want to proceed with segments from a long recording. The format is like this:
```
UTT_ID1 WAV_ID1 START_UTT1 END_UTT1
UTT_ID2 WAV_ID1 START_UTT2 END_UTT2
UTT_ID3 WAV_ID2 START_UTT3 END_UTT3
...
```

#### 3.2.4 other requirements

The indexing files are supposed to be sorted in a specific order. Meanwhile, there are fix and checking scripts for the data directory. In general, you can follow the following scripts:
```
export LC_ALL=C
for x in train dev test; do
  sort data/${x}/text -o data/${x}/text
  utils/fix_data_dir.sh data/${x}
  utils/validate_data_dir.sh data/${x}
done
```

### 3.3. Training model

The training procedure in ESPnet is simple. Just following the stages in `asr.sh` would be fine. We can define the network structure and its corresponding training arguments in `conf/train_asr.yaml`. Followings are some example model architectures and training options:

- [Conformer Architecture with Self-supervised Representations (Latest)](https://github.com/espnet/espnet/blob/master/egs2/librispeech/asr1/conf/tuning/train_asr_conformer7_hubert_960hr_large.yaml)
- [Conformer Architecture](https://github.com/espnet/espnet/blob/master/egs2/commonvoice/asr1/conf/tuning/train_asr_conformer5.yaml)
- [Transformer Architecture](https://github.com/espnet/espnet/blob/master/egs2/commonvoice/asr1/conf/tuning/train_asr_transformer.yaml)
- [RNN Architecture](https://github.com/espnet/espnet/blob/master/egs2/commonvoice/asr1/conf/tuning/train_asr_rnn.yaml)


To get a taste of how the performances of each model on various tasks, you may either check the `egs2/${dataset}/RESULTS.md` or the following papers:

- [Self-supervised Representation](https://arxiv.org/abs/2110.04590)
- [Conformer v.s. Transformer](https://arxiv.org/abs/2010.13956)
- [Transformer v.s. RNN](https://merl.com/publications/docs/TR2019-158.pdf)


### 3.4. Evaluating Speech Recognition Accuracy

ESPnet can handle the decoding and scoring in the evaluation stages.
You need to first decode from the trained model. An example decoding configuration can be found in [here](https://github.com/espnet/espnet/blob/master/egs2/commonvoice/asr1/conf/tuning/decode_transformer.yaml).

The scoring stage results in a table with detailed error rate calculation. The following is an example:
```
## asr_train_asr_conformer5_raw_cy_bpe150_sp
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_lm_lm_train_lm_cy_bpe150_valid.loss.ave_asr_model_valid.acc.ave/dev_cy|2933|28498|88.3|10.3|1.4|1.1|12.8|48.1|
|decode_asr_lm_lm_train_lm_cy_bpe150_valid.loss.ave_asr_model_valid.acc.ave/test_cy|2937|26046|91.9|7.2|0.9|0.7|8.8|27.3|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_lm_lm_train_lm_cy_bpe150_valid.loss.ave_asr_model_valid.acc.ave/dev_cy|2933|156313|96.5|1.9|1.7|0.9|4.4|48.1|
|decode_asr_lm_lm_train_lm_cy_bpe150_valid.loss.ave_asr_model_valid.acc.ave/test_cy|2937|139576|97.2|1.5|1.3|0.7|3.5|27.3|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_lm_lm_train_lm_cy_bpe150_valid.loss.ave_asr_model_valid.acc.ave/dev_cy|2933|94018|93.9|3.9|2.2|0.9|7.0|48.1|
|decode_asr_lm_lm_train_lm_cy_bpe150_valid.loss.ave_asr_model_valid.acc.ave/test_cy|2937|83456|95.5|2.9|1.6|0.8|5.3|27.3|
```

Normally, we use CER or WER for ASR evaluation. They are defined based on edit distance between reference and source transcription.

## 5. Improving Your System

Depending on the scenarios, we can further improve your system by different methods.

### 5.1 Hyper-parameter tuning

Hyper-parameter tuning could be a good start to improve the system. We recommend the following parameters to tune in the training config (i.e., `conf/train_asr.yaml`):
```
optim_conf.lr               # peak learning rate for optimizer (can be large if it is slow to converge)
scheduler_conf.warmup_steps # warmup steps (should be smaller for small corpora)
batch_size                  # batch size (a larger batch size could be helpful sometimes)
                            # depends on the sampler, it might be in different names
init                        # parameter initialization strategies
patience                    # early stop patience
model_conf.ctc_weight       # CTC weight for CTC/Attention hybrid training
encoder_conf.num_blocks     # number of layers for encoder
encoder_conf.dropout        # dropout rate for encoder linear layers
encoder_conf.attention_dropout_rate  # dropout rate for attention weights
encoder_conf.cnn_module_kernel       # only for Conformer models
```

### 5.2 Pre-training
Another method is to adopt pre-trained models. Even if the language is endangered, it may share some common features as other languages. Therefore, we often observe better ASR systems with pre-trained models, especially for small corpora. 

As for new languages, we recommend [open_li52](https://zenodo.org/record/4509663), which is a multilingual speech recognition model trained in over 50 languages.

To adopt the pre-trained model to ESPNet training, you simply need to add arguments to `run.sh` as:
```
    --pretrained_model /path/to/model.pth  # the pth file of the pretrained model.
    --ignore_init_mismatch true            # if the model architecture is exactly the same, it can be set as "false"
```

### 5.3 Self-supervised representation
Another possibility is to use self-supervised representation, which takes benefit from large-scale untranscribed data. ESPNet has a tight collaboration with [S3PRL](https://github.com/s3prl/s3prl) which offers various latest self-supervised representation extraction. To add them into the training, please see this [example](https://github.com/espnet/espnet/blob/master/egs2/librispeech/asr1/conf/tuning/train_asr_conformer7_hubert_960hr_large.yaml).

### 5.4 Other resources
It's also good to incorporate other resources: additional data, additional text for language modeling, data augmentation, adding synthetic data, etc.

## 6. Reference

### 6.1 Datasets
- Chen, G., Chai, S., Wang, G., Du, J., Zhang, W.Q., Weng, C., Su, D., Povey, D., Trmal, J., Zhang, J. and Jin, M., 2021. GigaSpeech: An Evolving, Multi-domain ASR Corpus with 10,000 Hours of Transcribed Audio. arXiv preprint arXiv:2106.06909.
- Zhang, B., Lv, H., Guo, P., Shao, Q., Yang, C., Xie, L., Xu, X., Bu, H., Chen, X., Zeng, C. and Wu, D., 2021. WenetSpeech: A 10000+ Hours Multi-domain Mandarin Corpus for Speech Recognition. arXiv preprint arXiv:2110.03370.
- rdila, R., Branson, M., Davis, K., Kohler, M., Meyer, J., Henretty, M., Morais, R., Saunders, L., Tyers, F. and Weber, G., 2020, May. Common Voice: A Massively-Multilingual Speech Corpus. In Proceedings of the 12th Language Resources and Evaluation Conference (pp. 4218-4222).
- Black, A.W., 2019, May. Cmu wilderness multilingual speech dataset. In ICASSP 2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 5971-5975). IEEE.

### 6.2 Toolkits
- Watanabe, S., Hori, T., Karita, S., Hayashi, T., Nishitoba, J., Unno, Y., Enrique Yalta Soplin, N., Heymann, J., Wiesner, M., Chen, N., Renduchintala, A., Ochiai, T. (2018) ESPnet: End-to-End Speech Processing Toolkit. Proc. Interspeech 2018, (pp. 2207-2211)
- Watanabe, S., Boyer, F., Chang, X., Guo, P., Hayashi, T., Higuchi, Y., Hori, T., Huang, W.C., Inaguma, H., Kamo, N. and Karita, S., 2021, June. The 2020 espnet update: new features, broadened applications, performance improvements, and future plans. In 2021 IEEE Data Science and Learning Workshop (DSLW) (pp. 1-6). IEEE.
- Povey, D., Ghoshal, A., Boulianne, G., Burget, L., Glembek, O., Goel, N., Hannemann, M., Motlicek, P., Qian, Y., Schwarz, P. and Silovsky, J., 2011. The Kaldi speech recognition toolkit. In IEEE 2011 workshop on automatic speech recognition and understanding (No. CONF). IEEE Signal Processing Society.
- https://github.com/wiseman/py-webrtcvad

### 6.3 Methodology
- Graves, A., Fernández, S., Gomez, F. and Schmidhuber, J., 2006, June. Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks. In Proceedings of the 23rd international conference on Machine learning (pp. 369-376).
- Chorowski, J., Bahdanau, D., Serdyuk, D., Cho, K. and Bengio, Y., 2015, December. Attention-based models for speech recognition. In Proceedings of the 28th International Conference on Neural Information Processing Systems-Volume 1 (pp. 577-585).
- Watanabe, S., Hori, T., Kim, S., Hershey, J.R. and Hayashi, T., 2017. Hybrid CTC/attention architecture for end-to-end speech recognition. IEEE Journal of Selected Topics in Signal Processing, 11(8), pp.1240-1253.
- Karita, S., Chen, N., Hayashi, T., Hori, T., Inaguma, H., Jiang, Z., Someki, M., Soplin, N.E.Y., Yamamoto, R., Wang, X. and Watanabe, S., 2019, December. A comparative study on transformer vs rnn in speech applications. In 2019 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU) (pp. 449-456). IEEE.
- Gulati, A., Qin, J., Chiu, C.-C., Parmar, N., Zhang, Y., Yu, J., Han, W., Wang, S., Zhang, Z., Wu, Y., Pang, R. (2020) Conformer: Convolution-augmented Transformer for Speech Recognition. Proc. Interspeech 2020, (pp. 5036-5040).
- Dong, L., Xu, S. and Xu, B., 2018, April. Speech-transformer: a no-recurrence sequence-to-sequence model for speech recognition. In 2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 5884-5888). IEEE.
- Yang, S.-w., Chi, P.-H., Chuang, Y.-S., Lai, C.-I.J., Lakhotia, K., Lin, Y.Y., Liu, A.T., Shi, J., Chang, X., Lin, G.-T., Huang, T.-H., Tseng, W.-C., Lee, K.-t., Liu, D.-R., Huang, Z., Dong, S., Li, S.-W., Watanabe, S., Mohamed, A., Lee, H.-y. (2021) SUPERB: Speech Processing Universal PERformance Benchmark. Proc. Interspeech 2021, (pp. 1194-1198).
- Chang, X., Maekaku, T., Guo, P., Shi, J., Lu, Y.J., Subramanian, A.S., Wang, T., Yang, S.W., Tsao, Y., Lee, H.Y. and Watanabe, S., 2021. An exploration of self-supervised pretrained representations for end-to-end speech recognition. arXiv preprint arXiv:2110.04590.
- Watanabe, S., Hori, T. and Hershey, J.R., 2017, December. Language independent end-to-end architecture for joint language identification and speech recognition. In 2017 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU) (pp. 265-271). IEEE.
- Hou, W., Dong, Y., Zhuang, B., Yang, L., Shi, J. and Shinozaki, T., 2020. Large-Scale End-to-End Multilingual Speech Recognition and Language Identification with Multi-Task Learning. Proc. Interspeech 2020 (pp. 1037-1041).
