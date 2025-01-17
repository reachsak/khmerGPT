from whisper_cpp_python import Whisper
from whisper_cpp_python.whisper_cpp import whisper_progress_callback

def callback(ctx, state, i, p):
    print(i)

model = Whisper('../quantized_models/whisper/models/ggml-tiny.bin')
model.params.progress_callback = whisper_progress_callback(callback)

print(model.transcribe('vendor/whisper.cpp/samples/jfk.wav'))