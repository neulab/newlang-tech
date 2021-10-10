# Selecting good prompts
By now you have a dataset(s) with text from which you want to select the best sentences(prompts) to build your speech corpus. This section takes you through how to obtain the best utterances from your dataset(s). Most of the information here is obtained from [the corpus development chapter](http://festvox.org/bsv/c2176.html) where you can find detailed explanations.

**What makes a good prompts set?**
* Phonetically and prosodically balanced
* Targeted toward the intended domain(s)
* Easy to say by voice talent without mistakes
* Short enough for the voice talent to be willing to say it.
## Install the tools
The tools needed run on a Linux environment. If you do not have one and are using Windows OS you can install Ubuntu app and use it by following instructions on [the official documentation](https://ubuntu.com/tutorials/ubuntu-on-windows#1-overview).
###Prerequisites
After you have your Linux environment and terminal set up, do the following to install ubuntu packages:
```
sudo apt-get install git build-essential libncurses5-dev sox wget
sudo apt-get install csh ffmpeg html2text
```
###Clone the repository
```
git clone https://github.com/festvox/datasets-CMU_Wilderness
cd datasets-CMU_Wilderness
```
###Make dependencies
```
./bin/do_found make_dependencies
```

### Add Festvox and Speech Tools to path
You need to add Festvox and Edinburgh Speech tools to your environment variables so that they can work properly.
Replace path in the following commands with the path to your ``datasets-CMU_Wilderness`` directory. 
```
export FESTVOXDIR=/path/build/festvox
export ESTDIR=/path/build/speech_tools
```
##Run the tools

Follow the steps below to obtain a set of good sentences from your dataset(s).You can have your data in one file or in many files. Working files will be created in the current directory so if you were still in the ``datasets-CMU_Wilderness`` directory you need to change to 
your preferred storage location. 

*Hint*: If you are using WSL(Ubuntu on Windows) you can access your Windows file system by ``\mnt\c``.

### 1. Find word frequencies of all the tokens in the text data
TEXT0.txt TEXT1.txt are the names of your files. 
```
$FESTVOXDIR/src/promptselect/make_nice_prompts find_freq TEXT0.txt TEXT1.txt TEXT2.txt
```
### 2. Build a Festival lexicon for the most frequent words
The default is to select top 5000 words, which you can override by adding the number you want as an argument.
```
$FESTVOXDIR/src/promptselect/make_nice_prompts make_freq_lex   ##default
$FESTVOXDIR/src/promptselect/make_nice_prompts make_freq_lex 2000

```
### 3. Find nice utterances
This step can take a number of hours to finish processing.
```
$FESTVOXDIR/src/promptselect/make_nice_prompts find_nice TEXT0 TEXT1 ...
```
The 'nice' utterances can be found in ``data_nice.data`` file in your current directory.
It is worth going through the sentences selected and figuring out if they are good enough to be in the final prompt set. Based on your findings you might want to run the process all over again to look for a different outcome.
### 4. A shortcut
You can do the whole process with: 
``` $FESTVOXDIR/src/promptselect/make_nice_prompts do_all_asis TEXT0.txt TEXT1.txt```

## Non-Latin Script
For non-Latin languages with spaces between words and are UTF-encoded eg Arabic and Hindi use:
```
    $FESTVOXDIR/src/promptselect/make_nice_prompts select_seg
    $FESTVOXDIR/src/promptselect/make_nice_prompts find_freq_asis TEXT0 TEXT1 ...
    $FESTVOXDIR/src/promptselect/make_nice_prompts make_freq_lex
    $FESTVOXDIR/src/promptselect/make_nice_prompts find_nice_asis TEXT0 TEXT1 ...
    $FESTVOXDIR/src/promptselect/make_nice_prompts select_letter_n
    $FESTVOXDIR/src/promptselect/make_nice_prompts find_vocab_asis
```

## Acknowledgements
We would like to thank CMU Wilderness Project and Prof Alan W. Black for the tools and documentation.
