import json
import os
import logging
import re

from kalliope.core import Utils
from kalliope.core.ConfigurationManager import BrainLoader

from vosk import Model, KaldiRecognizer, SetLogLevel

from kalliope.stt.Utils import SpeechRecognition


logging.basicConfig()
logger = logging.getLogger("kalliope")



class Vosk(SpeechRecognition):

    kaldirecognizer = None

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Vosk
        :param callback: The callback function to call to send the text
        :param kwargs:
        """

        SpeechRecognition.__init__(self, kwargs.get('audio_file_path', None))
        log_level = kwargs.get('log_level', -99)
        if log_level == -99:
            if logger.isEnabledFor(logging.DEBUG):
                log_level = 0
        SetLogLevel(log_level)

        self.main_controller_callback = callback
        self.model_path = kwargs.get('model_path', None)
        self.grammar_calculate = kwargs.get('calculate_grammar', True)

        if self.grammar_calculate:
            logger.debug("[vosk] generating kaldi grammar from all synapse orders and variables:")
            self.grammar_calculated = []
            brainloader = BrainLoader()
            brain = brainloader.brain
            for synapse in brain.synapses:
                for signal in synapse.signals:
                    if signal.name == "order":
                        self.grammar_calculated.append(re.sub('{{.+}}', '', signal.parameters).lower())
                        logger.debug("[vosk] - adding order '%s' to grammar" % signal.parameters.lower())
            self._recursively_add_variable_leafs(brainloader.settings.variables)

        klass = self.__class__
        if not hasattr(klass, 'model'):
            klass.model = {}
        if self.model_path not in klass.model:
            logger.debug("[vosk] model '%s' is not found in the class cache" % self.model_path)
            if self.model_path is None or os.path.exists(self.model_path) == False:
                Utils.print_danger("Please configure parameter 'model_path' to a valid language model")
                exit (1)
            logger.info('[vosk] Loading model...')
            klass.model[self.model_path] = Model(self.model_path)
            logger.debug("[vosk] model '%s' is added to the class cache" % self.model_path)
        if self.grammar_calculate:
            for i, item in enumerate(self.grammar_calculated):
                item = re.sub(r'[0-9!-/:-@[-`{-~]', ' ', item)
                self.grammar_calculated[i] = item
            self.grammar_calculated = list(set(" ".join(set(self.grammar_calculated)).split()))
            self.grammar_calculated.sort()
            logger.debug("[vosk] applying the calculated grammar for KaldiRecognizer: %s" % (self.grammar_calculated))
            if self.kaldirecognizer is None:
                self.kaldirecognizer = KaldiRecognizer(klass.model[self.model_path], 16000, json.dumps(self.grammar_calculated, ensure_ascii=False))
        else:
            logger.debug("[vosk] using the grammar dictionary of the model for KaldiRecognizer")
            if self.kaldirecognizer is None:
                self.kaldirecognizer = KaldiRecognizer(klass.model[self.model_path], 16000)
        self.set_callback(self.vosk_callback)
        self.start_processing()


    def vosk_callback(self, recognizer, audio_data):
        wav = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        self.kaldirecognizer.AcceptWaveform(wav)
        result = json.loads(self.kaldirecognizer.FinalResult())
        logger.debug("[vosk] KaldiRecognizer.FinalResult() returned '%s'" % result['text'])
        captured_audio = result['text']
        Utils.print_success("Vosk thinks you said '%s'" % captured_audio)
        self._analyse_audio(captured_audio)


    def _analyse_audio(self, audio_to_text):
        """
        Confirm the audio exists and run it in a Callback
        :param audio_to_text: the captured audio
        """
        if self.main_controller_callback is not None:
            self.main_controller_callback(audio_to_text)


    def _recursively_add_variable_leafs(self, variables):
        for variable in variables:
            value = None
            if isinstance(variables, dict):
                value = variables[variable]
                if isinstance(value, str):
                    value = value.lower()
                    logger.debug("[vosk] - adding '%s' from variables to grammar" % (value))
                    self.grammar_calculated.append(value)
                if isinstance(value, list) or isinstance(value, dict):
                    self._recursively_add_variable_leafs(value)
            if isinstance(variable, str):
                value = variable.lower()
                logger.debug("[vosk] - adding '%s' from variables to grammar" % (value))
                self.grammar_calculated.append(value)
            if isinstance(variable, list) or isinstance(variable, dict):
                self._recursively_add_variable_leafs(variable)
