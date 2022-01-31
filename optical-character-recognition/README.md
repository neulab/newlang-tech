# Building Optical Character Recognition for New Languages

Optical character recognition (OCR) is the task of extracting text from scanned images of printed, typed, or handwritten documents. It is an essential first step to apply downstream technologies that require the text to be in a machine-readable format, such as automatic search, machine translation, text analytics, and practically any other NLP task.

OCR models rely on visual information from the image (shape of the alphabet, spacing, etc.) and language information (context of each character) to produce a transcription of the text contained in an image.

This document covers multiple methods to perform OCR on documents in a new language. Some of these methods require training a machine learning model, but there are off-the-shelf OCR tools that might also work well and are much easier to try as a first step.

## <a id="data"></a>Creating Data

To evaluate the performance of various OCR techniques, you will need an evaluation dataset that contains manually transcribed scanned images in the target language. The evaluation dataset should ideally be a diverse set of documents with various features/fonts/artifacts that may affect the OCR performance. 

OCR annotation can be conducted as follows:
* Given an image, the annotator is required to transcribe the text present in that image.
* The annotator should transcribe the text line-by-line.
* If the document contains multiple blocks of text (page title, multiple columns, footnotes, etc.), the annotator should segment bounding boxes before transcribing the text. This step may or may not be necessary depending on the specific document and your downstream application for the text.
    * A layout analysis tool like [LAREX](https://github.com/OCR4all/LAREX) can be used for semi-automatically extracting bounding boxes for complex layouts.
    * The text in each bounding box should be annotated separately.
* Note the [section on preprocessing](#preproc) below: if you plan to train your own OCR model, you may consider *automatically segmenting the pages into line images* and then doing annotation per line. This is not necessary for most pretrained tools/models since they internally perform segmentation.

[Label Studio](https://labelstud.io) is an open-source annotation tool that has a ready-to-use OCR annotation format.

If a large number of pages can be annotated, then the data can be split into training and evaluation sets for training a *supervised* machine learning model for OCR. If only a small evaluation set is available, off-the-shelf tools or *unsupervised* OCR can be used.


## Off-the-shelf OCR Tools

There are many off-the-shelf OCR tools that have pretrained models for 80-100 languages in a variety of scripts. If your target language is supported by one of these tools, it is recommended to use these pretrained models directly, since they are typically high performance.

Even if the language you are trying to build OCR for is not directly supported by these tools, you may find that they perform reasonably well if they are pretrained on languages that use the same character set (i.e., the same script) as your target language.
For example, an OCR model trained on Hindi might work well for Nepali since they both use the Devanagari writing system.
The OCR won't be perfect because the model will rely only on visual information to produce the text, but applying these tools is a straightforward method to get an *initial transcription*.

Popular tools include:
* [Google Vision](https://cloud.google.com/vision/)
* [Tesseract](https://tesseract-ocr.github.io)
* [EasyOCR](https://github.com/JaidedAI/EasyOCR)

To use the Google Vision OCR tool, you can use the script and follow the instructions in [this repository](https://github.com/shrutirij/ocr-post-correction/blob/main/firstpass.md).

To improve the output from the pretrained model, you can use OCR post-correction as described in [this section](#ocr-post).

## Training an OCR Model

### <a id="preproc"></a>Preprocessing

Training an OCR system often needs the scanned image to be segmented into lines with the corresponding annotation for each line as the training/evaluation datasets, which is why the [data creation section](#data) above recommends line-by-line annotation.

* [Kraken](http://kraken.re/master/index.html) can be used to automatically segment each page into line images.

## Training a Supervised OCR Model

There are many existing OCR software packages for training a new model in your target language if you have enough annotated data for supervised machine learning. 

* EasyOCR describes how to build a new OCR model [here](https://github.com/JaidedAI/EasyOCR/blob/master/custom_model.md) using the technique presented in the [deep text recognition benchmark](https://github.com/clovaai/deep-text-recognition-benchmark).
* Tesseract has instructions for training a custom model [here](https://github.com/tesseract-ocr/tesstrain).


## Training an Unsupervised OCR Model

If you do not have transcribed images for training, but have unlabeled text in the target language (e.g., from Wikipedia, the Common Crawl, or any other text source), you can use unsupervised learning.

* [Ocular](https://github.com/tberg12/ocular) is a tool to train an unsupervised OCR system using a language model trained on the unlabeled text in the target language.
    * It is known to perform reasonably well even for low-resource settings where not much unlabeled text is available.

## <a id="ocr-post"></a>Improving Performance with Automatic Post-Correction

The results from OCR systems (both off-the-shelf and if you train a new model) can be improved through the process of OCR post-correction. Training a post-correction model often requires much less annotated data for improved performance.

* [This repository](https://github.com/shrutirij/ocr-post-correction) has instructions and software to train a post-correction model for low-resource languages. 
    * If all available manual annotations are being used as the evaluation dataset (i.e., a low-resource setting), the post-correction model can be trained with k-fold cross-validation to estimate performance and then retrained on the whole dataset for applying on unlabeled documents.

## Evaluation

OCR transcriptions are typically evaluated using character error rate (CER) and word error rate (WER), which measure the fraction of incorrect characters or words in the predicted transcription as compared to the manual annotation of the document. 

A simple python function to calculate these metrics can be found [here](https://github.com/shrutirij/ocr-post-correction/blob/main/utils/metrics.py).
