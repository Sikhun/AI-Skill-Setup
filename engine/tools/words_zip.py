"""Exact per-character times for each phrase with the sherpa-onnx Thai zipformer (model in ~/asr or $ASR_MODEL).
Rewrites transcript.json tokens as [time, cumulative text] with asr = script text, so W() uses real times."""
import sherpa_onnx, wave, json, re, difflib, subprocess, tempfile, numpy as np, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Model folder: $ASR_MODEL, else ~/asr/<model>, else /tmp/asr/<model>
M=os.environ.get("ASR_MODEL") or next((d for d in [os.path.expanduser("~/asr/sherpa-onnx-zipformer-thai-2024-06-20"),"/tmp/asr/sherpa-onnx-zipformer-thai-2024-06-20"] if os.path.isdir(d)), None)
if not M: raise SystemExit("Thai ASR model not found: unpack sherpa-onnx-zipformer-thai-2024-06-20 into ~/asr/ (see SETUP.md) or set ASR_MODEL")
M=os.path.join(M,"")
V16=os.path.join(tempfile.gettempdir(),"vo16.wav")
r=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=M+"encoder-epoch-12-avg-5.int8.onnx",decoder=M+"decoder-epoch-12-avg-5.int8.onnx",joiner=M+"joiner-epoch-12-avg-5.int8.onnx",tokens=M+"tokens.txt",num_threads=4,decoding_method="greedy_search")
tr=json.load(open(f"{R}/transcript.json"))
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{R}/{tr['audio']}","-ar","16000","-ac","1","-c:a","pcm_s16le",V16],check=True)
w=wave.open(V16);sr=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
norm=lambda s: re.sub(r"[\s\"'.,!?…ๆ+]","",s)
for p in tr["phrases"]:
    s0=max(0,p["start"]-0.05); st=r.create_stream(); st.accept_waveform(sr,a[int(s0*sr):int((p["end"]+0.1)*sr)]); r.decode_stream(st)
    hyp="";ht=[]; tk=list(zip(st.result.tokens,st.result.timestamps))
    for j,(t,ts) in enumerate(tk):
        t=t.replace("ํา","ำ").replace("▁","").replace(" ",""); nxt=tk[j+1][1] if j+1<len(tk) else ts+0.25
        for c,ch in enumerate(t): hyp+=ch; ht.append(s0+ts+(nxt-ts)*c/max(1,len(t)))
    txt=norm(p["text"]); xs=[];ys=[]
    for b in difflib.SequenceMatcher(None,txt,hyp,autojunk=False).get_matching_blocks():
        for q in range(b.size): xs.append(b.a+q); ys.append(ht[b.b+q])
    if not xs: xs,ys=[0,len(txt)-1],[p["start"],p["end"]]
    T=np.interp(range(len(txt)),xs,ys); T=np.maximum.accumulate(T)
    p["asr"]=p["text"]; p["tokens"]=[[round(float(T[i]),3),txt[:i+1]] for i in range(len(txt))]
    print(p["n"],f"{len(xs)}/{len(txt)} anchored",p["text"][:30])
json.dump(tr,open(f"{R}/transcript.json","w"),ensure_ascii=False,indent=1)
