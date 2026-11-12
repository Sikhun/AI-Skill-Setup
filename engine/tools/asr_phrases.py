"""Recognise each tightened phrase with the sherpa-onnx Thai zipformer (~/asr or $ASR_MODEL) -> prints n, times, text."""
import sherpa_onnx, wave, json, subprocess, tempfile, numpy as np, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Model folder: $ASR_MODEL, else ~/asr/<model>, else /tmp/asr/<model>
M=os.environ.get("ASR_MODEL") or next((d for d in [os.path.expanduser("~/asr/sherpa-onnx-zipformer-thai-2024-06-20"),"/tmp/asr/sherpa-onnx-zipformer-thai-2024-06-20"] if os.path.isdir(d)), None)
if not M: raise SystemExit("Thai ASR model not found: unpack sherpa-onnx-zipformer-thai-2024-06-20 into ~/asr/ (see SETUP.md) or set ASR_MODEL")
M=os.path.join(M,"")
V16=os.path.join(tempfile.gettempdir(),"vo16.wav")
r=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=M+"encoder-epoch-12-avg-5.onnx",decoder=M+"decoder-epoch-12-avg-5.onnx",joiner=M+"joiner-epoch-12-avg-5.onnx",tokens=M+"tokens.txt",num_threads=4,decoding_method="modified_beam_search")
tm=json.load(open(f"{R}/tools/tight-map.json"))
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{R}/assets/audio/derived/vo-tight.wav","-ar","16000","-ac","1","-c:a","pcm_s16le",V16],check=True)
w=wave.open(V16);sr=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
for p in tm["phrases"]:
    st=r.create_stream(); st.accept_waveform(sr,a[int(max(0,p["start"]-0.05)*sr):int((p["end"]+0.1)*sr)]); r.decode_stream(st)
    print(p["n"], f'{p["start"]:.2f}-{p["end"]:.2f}', st.result.text.replace(" ",""))
