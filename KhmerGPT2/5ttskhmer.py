import os
import azure.cognitiveservices.speech as speechsdk


speech_config = speechsdk.SpeechConfig(subscription="5630d19384fc422f88c86b91e2354aee", region="eastus")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


speech_config.speech_synthesis_voice_name='km-KH-PisethNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


text = "មានប្រទេសសំខាន់ពីរហៅថា អាមេរិក៖ ១. **អាមេរិកខាងជើង**៖ ទ្វីបនេះ ជាទឹកដីរបស់សហរដ្ឋអាមេរិក (ស.រ.អា), កាណាដា ម៉ិកស៊ិក និងប្រទេសមួយចំនួនទៀត។ ២. **អាមេរិកខាងត្បូង**៖ ទ្វីបនេះ ជាទឹកដីរបស់ប្រទេសដូចជា ប្រេស៊ីល អាហ្សង់ទីន ឈីលី និងប្រទេសជាច្រើនទៀត។  ដូច្នេះ វា អាស្រ័យ ទៅ លើ អ្វី ដែល អាមេរិក អ្នក កំពុង សំដៅ ទៅ៖ * ប្រសិន បើ អ្នក ចង់ មាន ន័យ ថា ដី នៅ ប៉ែក ខាង លិច ដែល គេ ស្គាល់ ជា ទូទៅ ថា ជា ទ្វីប អាមេរិក នោះ គឺ ស្ថិត នៅ ក្នុង ទ្វីប **អាមេរិក ខាង ជើង** ។ * ប្រសិនបើលោកអ្នកចង់មានន័យថា ដីនៅភាគខាងត្បូងដែលតែងសំដៅទៅអាមេរិកខាងត្បូង នោះវាក៏ស្ថិតនៅក្នុងទ្វីប **អាមេរិកខាងត្បូង** ផងដែរ។"


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
