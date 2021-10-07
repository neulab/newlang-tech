# Building Speech Synthesis for New Languages

Speech synthesis is the task of generating speech from text. It is useful if you want to build a speech interface.
For a speech synthesizer, we usually require voice recordings from one person.

## Collecting Data

There are many sources for speech data that can be used to train systems. It'd be a good idea to take a look here to see if there is data that you can use.

* [CMU Wilderness Corpus](https://github.com/festvox/datasets-CMU_Wilderness): This is a very broad corpus with 699 languages.

## Creating Data
The goal here is to create a speech corpus of aligned speech recordings and their transcriptions to be used to build the synthesizer. 
1. Gather textual sentences in your language. You should aim at getting atleast 1 million words. Keep in mind:
   - The copyright of the data you have gathered; make sure it is sufficient for your usage and distribution needs
   - The text should be in the same encoding
2. Select good sentences from this corpus to be used  to build your synthesizer. There is documentation on how to do it [here](http://festvox.org/bsv/c2176.html).
You will need software to run the instructions on the documentation. Follow the instructions [here from CMU Wilderness](https://github.com/festvox/datasets-CMU_Wilderness) from *Prerequisites* to *Make Dependencies* sections.
At the end of these steps, you should have your recorded speech corpus ready for the next step.
3. Identify a voice talent who is fluent in the language you are working on.
4. Record the selected sentences.
### Recording tips
* There should be little to no noise, a studio environment is best
* If you are using a mobile device, you can use an app that will save your recordings in .wav format. For iOS you can use [one of these apps](https://www.iosappweekly.com/record-sound-mp3-wav-format-iphone/) for example.
* The distance between the speaker and the microphone should be constant, so it is best to use a microphone attached to the speakers head for example using headsets or AirPods
* If you are going to record in multiple sessions, record at the same time period to avoid variations in the voice eg at 11:00 am - 12:30 pm for all your sessions.
* The utterances should be consistent in terms of speed etc. Avoid excited speech as it has a lot of variations
* If you are recording a bunch of sentences continuously in one recording, make sure the voice talent gives a hint as to which sentence they are reading such that it will be easier to process eg " [pause from last sentence, sentence8] sentence9 [pause] This is sentence9 that I am reading"
## Training a Speech Synthesizer


TODO: This should be filled in.

## Evaluating Synthesizer Accuracy

TODO: Evaluating synthesizer accuracy info.

## Improving Your System

TODO: Once the system is created, there are several ways to improve it.
