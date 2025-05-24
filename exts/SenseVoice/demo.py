from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

def init_model():
    model = AutoModel(
        model="F:\DjangoRestfulAPI\s2i\exts\SenseVoice",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
        hub="hf",
        disable_update=True,
    )
    return model
def generate_text(model,file_path):
    # en
    res = model.generate(
        input=file_path,
        cache={},
        language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  #
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    print(text)
    return text

