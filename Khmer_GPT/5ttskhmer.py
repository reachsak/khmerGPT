import os
import azure.cognitiveservices.speech as speechsdk


speech_config = speechsdk.SpeechConfig(subscription="5630d19384fc422f88c86b91e2354aee", region="eastus")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


speech_config.speech_synthesis_voice_name='km-KH-PisethNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


text = "ខ្ញុំ បាន ទទួល បញ្ជា មួយ ដើម្បី បិទ ភ្លើង នៅ ក្នុង បន្ទប់ ។ ពន្លឺ បាន បិទ"


speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
