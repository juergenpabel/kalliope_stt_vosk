# kalliope-vosk
Kalliope module for STT with VOSK (https://github.com/alphacep/vosk-api/)

## Synopsis
Speech-to-text in kalliope with VOSK (based on kaldi)

## Preparation
Before any module installation you have to check that you have defined the installation path for (at least SST) modules.
To do this, you must modify the settings.yml file and activate the "resource_directory" by adapting the path (for at least sst).
```bash
resource_directory:
  stt: "resources/stt"
```

## Install
```bash
kalliope install --git-url https://github.com/juergenpabel/kalliope-vosk.git
```

Change default STT to VOSK in settings.yml
```yml
default_speech_to_text: "vosk"
```


## Language model
This repository is a fork of https://github.com/veka-server/kalliope-vosk; in that repository a basic french language model is included - this fork does not contain any language models at all.

Download and install a language model you like (https://alphacephei.com/vosk/models). Unzip it and remember its path because you will have to add it to the settings.yml file afterwards. It is recommended to place the language model also in the corresponding resource directory for STT (see above).


Change default STT to VOSK in settings.yml
```yml
  - vosk:
      language: "<relative or absolute directory path to your language model>"
```


## Uninstall
```bash
kalliope uninstall --stt-name vosk
pip3 uninstall vosk
```
