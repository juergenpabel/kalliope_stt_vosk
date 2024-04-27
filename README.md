# kalliope_stt_vosk
Kalliope module for STT with VOSK (https://github.com/alphacep/vosk-api/)
It is originally a fork of https://github.com/veka-server/kalliope-vosk but with major changes/developments.

## Synopsis
Speech-to-text in kalliope with VOSK (based on kaldi)

## Preparation
Before any module installation you have to check that you have defined the installation path for (at least STT) modules.
To do this, you must modify the settings.yml file and activate the "resource_directory" by adapting the path (for at least STT).
```bash
resource_directory:
  stt: "resources/stt"
```

## Install
```bash
kalliope install --git-url https://github.com/juergenpabel/kalliope_stt_vosk.git
```

Change default STT to VOSK in settings.yml:
```yml
default_speech_to_text: "vosk"
```


## Language model
This repository is a fork of https://github.com/veka-server/kalliope-vosk; in that repository a basic french language model is included - this fork does not contain any language models at all. Download and install a language model you like (https://alphacephei.com/vosk/models). It is recommended to place the language model also inside the resources directory structure.

Set language model (parameter "model_path") in settings.yml:
```yml
  - vosk:
      model_path: "<relative or absolute directory path to your language model>"
```

## Language model optimization
Due to the string based (vs. intent based) parsing of (by the STT engine transcribed) speech utterances into matching orders, the STT enging can actually calculate the full valid grammar set (words) by adding up all words from all existing orders and also adding all names and values of kalliope variables. (In other words: any words outside that word list would not be "understood" by kalliope order parser anyhow.) Therefore, this STT implementation __by default__ calculates the grammar set base on orders and variables present in kalliope (at the time of each STT invocation). It therefore reduces the languages grammar (the word list) from something like >100.000 entries to something like <1.000 entries (depends on your specific setup, of course).

The effect of the reduced grammar is: __almost 0% word error rate__ (tested over many days with the german language model "vosk-model-small-de-0.15" from model page from above, YMMV). Anyhow, this optimization can be disabled by setting *calculate_grammar* to *False* in settings.yml.

```yml
  - vosk:
      model_path: "<relative or absolute directory path to your language model>"
      calculate_grammar: False
```


## Uninstall
```bash
kalliope uninstall --stt-name vosk
pip3 uninstall vosk
```
