# Building Speech Synthesis for New Languages

Speech synthesis is the task of generating speech from text. It is useful if you want to build a speech interface.
For a speech synthesizer, voice recordings from one person is usually required for consistency and natural sounding output.

## 1. Collecting Data

There are many sources for speech data that can be used to train systems. It'd be a good idea to take a look here to see if there is data that you can use.

* [CMU Wilderness Corpus](https://github.com/festvox/datasets-CMU_Wilderness): This is a very broad corpus with 699 languages.

If there is none, follow the steps in *[Creating Data](#2-creating-data)* section to create a corpus.
## 2. Creating Data
The goal here is to create a speech corpus of aligned speech recordings and their transcriptions to be used to build the synthesizer. 
1. Gather textual sentences in your language. You should aim at getting atleast 1 million words. Keep in mind:
   - The copyright of the data you have gathered; make sure it is sufficient for your usage and distribution needs. [Click here](https://aclanthology.org/L18-1202/) for information on licensing for Natural language Processing.
   - The text should be in the same encoding, see [this resource](https://stackoverflow.com/questions/64860/best-way-to-convert-text-files-between-character-sets) for details on how you can convert between encodings.
2. Select sentences from this corpus to be used to build your synthesizer. There is a quick guide on how to do so [here](selecting-prompts.md). 
 For a detailed explanation, read [this documentation](http://festvox.org/bsv/c2176.html) on how to select "good" sentences
 and follow [these instructions](https://github.com/festvox/datasets-CMU_Wilderness) from CMU Wilderness project from the *Prerequisites* to the *Make Dependencies* sections to install software needed to run the instructions on the documentation.
3. Identify a voice talent (person whose voices are recorded and will be used to build the synthesizer) who is fluent in the language and/or domain you are working on. Details on considerations are [available here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/record-custom-voice-samples#choose-your-voice-talent).
4. Get consent from your voice talent allowing you to use their voice for your intended usage and distribution purposes. 
5. Guide available [here.](http://festvox.org/bsv/x794.html)
6. Record the selected sentences.

At the end of these steps, you should have your recorded speech corpus ready for the next step.

### Recording tips
* There should be little to no noise, a studio environment is best.
* If you are using a mobile device, you can use an app that will save your recordings in .wav format. 
For iOS you can use [one of these apps](https://www.iosappweekly.com/record-sound-mp3-wav-format-iphone/) for example.
* The distance between the voice talent's mouth and the microphone should be constant, so it is best to use a microphone attached to the speakers head for example using headsets or AirPods
* If you are going to record in multiple sessions, record at the same time period for all your sessions to avoid variations in the voice 
(e.g. at 10:00 am - 12:30 pm - this time is good because it is not right after one gets up and not late in the evening when one is tired, so one's voice is likely at its best).
* The utterances should be consistent in terms of speed etc. Avoid excited speech as it has a lot of variations. 
* If you are recording a bunch of sentences continuously in one recording, make sure the voice talent gives a hint as to which sentence they are reading such that it will be easier to process e.g. 
 
     " ... [PAUSE] sentence nine [PAUSE]  I looked for Mary and Samantha at the bus station. [PAUSE] sentence ten [PAUSE] Jacob stood on his tiptoes.[PAUSE]..... "
* [Click here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/record-custom-voice-samples#recording-your-script) for more tips.
## 3. Training a Speech Synthesizer
There are generally two approaches to building a speech synthesizer/Text-to-Speech(TTS):
1. Standard/traditional TTS: Uses statistical, traditional machine learning and programming techniques
2. Neural TTS: Uses deep learning techniques

In this guide we will build a speech synthesizer using the standard approach.
Specifically, we are going to build a grapheme based synthesizer as it is easier when you have limited resources. 
For detailed explanation, see the Festvox tutorial on [Grapheme-based synthesizer](http://festvox.org/bsv/c3485.html). 
### 3.1 Prepare your data
If you followed step two above, you have your script file with textual utterances and corresponding recorded wav files. 
#### a) Align your utterances and wav files
The first step is to make sure that your wav files are aligned with your script.  
Your script should be in the following format:
> ( new_0001 "text in your language ..." )
> 
>( new_0002 "more text in your language ..." )
* Start each sentence with a `(` and end with a `)` leaving spaces between the brackets and text following/before.
* Replace `new` with anything you want, eg your language code or domain, leaving no spaces in between.
* The utterance should be in quotation marks.
* Precede other quotation marks with a backslash (\\).

Proceed to rename your wav files with the corresponding name. Eg, the first audio will be `new_0001.wav`
#### b) Numbers and symbols
If your script contains digits 0-9 and symbols like $, %, replace them with their word equivalent.
> She gave me $200. - She gave me two hundred dollars.
> 
> My battery level is at 50%. - My battery level is at fifty percent

If you followed the [Selecting Good Prompts](selecting-prompts.md) guide you probably won't have these issues.
#### c) Acronyms
You might have  acronyms like *USA* in your utterances.
You might want to change the text to how it is pronounced in your language. For example in my language I would change:
> She travelled to USA -- She travelled to YU ES E"
#### d) Quotation marks
Quotation marks may appear in your direct speech sentences eg
> ( eng_003 "She said, "Make sure you escape quotation marks!"" )
> 
Escape them using a backslash (\) like this:

> ( eng_003 "She said, \"Make sure you escape quotation marks!\\"" )
#### e) Foreign words
In some languages, normal speech will have words from other languages. During recording, the challenge is whether to pronounce them like they are in the language of origin or following your target language's pronunciation. Either way, change the script to reflect how it was pronounced by the voice talent, eg "word" to "wad".

#### f) Variations in recorded audio
When your recordings were done in different sessions and/or different microphones or microphone distance, there most likely will be variations in the volume and other characteristics of the audio. You need to power normalize the recordings to reduce their effect.
Running `./bin/get_wavs recording/*.wav` as part of the steps that will be outlined below will do that for you.

After making all the necessary changes, name your script file as `txt.done.data`.

### 3.2. Set up your environment.
Set up the prerequisite libraries detailed in the prerequisites section of [Selecting Good Prompts](selecting-prompts.md/#prerequisites).

After that, download and run [festvox_setup.sh](http://tts.speech.cs.cmu.edu/awb/11-492/homework/tts/fest_build.sh).
On your terminal run:
```
chmod +x festvox_setup.sh
./festvox_setup.sh
```
If you are using OSX, running the script won't complete because of an error. Follow the [instructions](setup_festvox_osx.md) here to fix it.

### 3.3 Train your model
We will use a language called *new* and a voice talent with initials *spk* for this demo.
1. Export environment variables below by replacing PATH-TO with the location of the `build` folder that you set up above.
```angular2html
export ESTDIR=PATH-TO/build/speech_tools
export FESTVOXDIR=PATH-TO/build/festvox
export SPTKDIR=/PATH-TO/build/SPTK
export FLITEDIR=/PATH-TO/build/flite
```
2. Setup voice directory
This is where you will be building your voice from. Use the three letter representation of your language(new) and speaker(spk) to name it.
```angular2html
mkdir cmu_new_spk
cd cmu_new_spk
$FESTVOXDIR/src/clustergen/setup_cg cmu new spk
```

3. Copy txt.done.data and audio files to your voice directory
```
cp -p WHATEVER/txt.done.data etc/
cp -p WHATEVER/wav/*.wav recording/ 
 ```
4. Power normalize and prune silences
```angular2html
./bin/get_wavs recording/*.wav
./bin/prune_silence wav/*.wav
./bin/prune_middle_silences wav/*.wav
```
5. Build voice templates
```
$FESTVOXDIR/src/grapheme/make_cg_grapheme
```
6. Build a random forest based voice model 

This process consumes a lot of memory, make sure you have enough and can take around 15 hrs depending on the size of your prompt list.
```angular2html
nohup ./bin/build_cg_rfs_voice &
```
## 4. Evaluating Synthesizer Accuracy
When the building process is complete, you will have a test directory in your voice directory. 
Your synthesized voices can be found in `test/tts_rf3` directory.

To check the performance of the model, look at two files;
`mcd-base.out` and `mcd-rf3.out`. The last four lines in these files contain the metrics, see example below. 
```
all  mean 4.779275 std 307.545312 var 94584.118855 n 3149025
F0   mean 17.620242 std 16.647217 var 277.129829 n 125961
noF0 mean 0.230314 std 0.453159 var 0.205354 n 3023064
MCD  mean 6.465406 std 2.540568 var 6.454484 n 125961
```
Check the mean of `MCD` row (lower is better). The score in mcd-rf3.out should be lower than mcd-base.out and decent scores are lower than 7. MCD means lower than 6 are good and you should aim at getting there.
## 5. Improving Your System

Once the system is created, there are several ways to improve it. A major cause of bad scores is mismatch between your prompts and the audio recordings.

To identify which utterances might be causing the low score, synthesise all the prompts in your `txt.done.data` and generate MCD scores for each of them. 
Run:
```
 nohup ./bin/do_clustergen parallel utt_by_utt etc/txt.done.data
 nohup ./bin/do_clustergen utt_by_utt_score etc/txt.done.data
```
The commands above will create a list of your text ordered from good to bad in `etc/txt.done.data.ordered`. 
The last number before *)* in each line is the MCD score for that utterance. 
The MCD score is not absolute as shorter utterances tend to have lower MCDs.  
  
Utterances at the end of this file though are somehow bad (mismatch between what was spoken and what is in the .wav file). It can be hard to identify why but here are things to lookout for:
* Some words weren't spoken, were inserted or substituted by another word. This is especially common for contractions(going to/gonna), words with alternative pronunciations and rare words where the speaker will replace them with a common word. 
* The recording was cut abruptly (at the end or the beginning). This may happen during recording, file transfer or conversion to `wav` format. 
* Spelling errors. Eg for my example language `ng'` and `ng` represent different sounds so if the apostrophe was left out in txt.done.data there will be a mismatch.
* Some words were overstressed, lengthened or slowed down than normal eg in excited speech.
* Pauses which are too long or short/inconsistent.
* Bad quality recording with noise

**Solutions**

* In the case of mismatch or pruned audio, change your txt.done.data to reflect what was in the corresponding recording.
* Correct spelling errors in txt.done.data.
* For foreign words or abbreviations, change them to their pronunciation spelling eg `word` to `wad`. 
* If the recording was really bad, you can exclude it from `txt.done.data` in your next run.
* Get better quality recordings with less noise and more consistency if possible .

Repeat the training process after making these changes to improve your synthesizer.
## 6. Using and Porting your System to a Device
TODO : How to use flite for Android