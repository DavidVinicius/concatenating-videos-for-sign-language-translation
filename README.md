# Less is more concatenating videos for Sign Language Translation
This repository contains some scripts that was used at the work: Less is more concatenating videos for Sign Language Translation presented at SIBGRAPI 2024.


The goal of this repository is explain how get the videos from the V-LIBRASIL, how create sentences with the videos, and how concatening the features. We provide some scripts that we used to create our dataset using V-LIBRAS videos.

You can read our work at: https://arxiv.org/abs/2409.01506

for Quote our work:

>da Silva, David Vinicius, Valter Estevam, and David Menotti. "Less is more: concatenating videos for Sign Language Translation from a small set of signs." 2024 37th SIBGRAPI Conference on Graphics, Patterns and Images (SIBGRAPI). IEEE, 2024.

## What is V-LIBRASIL

V-LIBRASIL is a labeled dataset of videos with native and professional interpreters articulating words and expressions in Libras (Brazilian Sign Language). There are more than 1350 videos of differents signs and each sign has 3 interpreters totalizing more than 4000 videos of signs.

For Quote V-LIBRASIL:
>A. J. Rodrigues, “V-LIBRASIL: uma base de dados com sinais na língua
>brasileira de sinais (Libras),” Master’s thesis, Universidade Federal de
>Pernambuco, 2021


## Getting videos

The V-LIBRASIL videos are avaliable at the website of the work. You can access the videos using this [LINK](https://libras.cin.ufpe.br/).


### Getting individual videos from the website
On the website you can download individual videos choosing a sign and pressing the download button.

##### 1. Choosing a sign
![Choosing a sing](/images/choosing-a-sign.png)

##### 2. Pressing the download button
![Pressing the download button](/images/download-button.png)

### Getting videos using scrapping.

Another way to get the videos is using a script to download the videos. You can use the file **v-librasil.json** to facilitate the download of the videos.

```json
    {
        "sign": "THE_SIGN",
        "page_link": "WEBSITE_PAGE_OF_THE_SIGN",
        "interpreter": "INTERPRETER_OF_THE_SIGN",
        "video_name": "NAME_OF_THE_VIDEO",
        "video_url": "WEBSITE_URL_OF_THE_VIDEO"
    }
```

Here we have an example:

```json
{
    "sign": "Abacaxi",
    "page_link": "https://libras.cin.ufpe.br/sign/817",
    "interpreter": 2,
    "video_name": "20210127091036_6011583c87073.mp4",
    "video_url": "https://libras.cin.ufpe.br/storage/videos/20210127091036_6011583c87073.mp4"
},
```

You need to use the attributes sign and interpreter in the json to rename the video name when you download. You must to use the kebab convention if you want to use our script to generate sentences.

A possible suggestion for kebab convetion:

```python
def kebab_case(string):
  return "-".join(word.lower() for word in string.split(" "))
```

For example for the sign "abacaxi" with the interpreter 2, the name of the video will be:
- 2-abacaxi.mp4

## Augmentation videos
In addition to V-Librasil videos, we produce augmentation videos. We use [Vidaug](https://github.com/okankop/vidaug) Library to create these videos.

We use only this type of videos augmentations:
- upsample
- downsample
- horizontal-flip
- horizontal flip with downsample
- horizontal flip with upsample

In the final, a video it have six versions for word and interpreting considering the augmentation. For example:
- 2-abacaxi.mp4
- 2-abacaxi-upsample.mp4
- 2-abacaxi-downsample.mp4
- 2-abacaxi-horizontal-flip.mp4
- 2-abacaxi-horizontal-flip-downsample.mp4
- 2-abacaxi-horizontal-flip-upsample.mp4



## Extracting features
For extract the features of the videos we use the [i3D features](https://v-iashin.github.io/video_features/models/i3d/).

We extract the features for each videos using the parameters **stack_size=10** and **step_size=10**

## Creating sentences
For create the sentences, we use a list of selected words. You can use our list in the file 50-selected-words.txt

We classified the classes of the words and we create the sentence following this pattern:

Noun + Adjective + Verb + Adverb

You will note that in the list we use a tag to represent the class of the word. The meaning of the tags are:

- v: Verb
- n: Noun
- a: Adjective
- r: Adverb

You can use the file create_sentences_by_preselected_words.py to create the sentences.


## Concatenating features
After the sentences were created, we concatenated the individual videos of the words that composed the sentences. For instance, consider a sentence such as:

- Cachorro Bonito Gostar Muito

We took the features extracted from the videos that comprise this sentence and concatenated them to form the feature representation of the sentence. For example:

- 0-cachorro.mp4
- 0-bonito.mp4
- 0-gostar.mp4
- 0-muito.mp4

```
    Feature sentence = 0-cachorro.feature + 0-bonito.feature + 0-gostar.feature + 0-muito.feature
```

To concatenate the features, we used the script **concat_features_files.py**.

## Training
For training, we use the [BMT](https://github.com/v-iashin/BMT)