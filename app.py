from flask import Flask, send_from_directory, request, jsonify
import openai
import whisper
import os
import tempfile

openai.api_key = os.environ.get("OPENAI_API_KEY")

SHOULD_RUN_LOCALLY = os.environ.get("USE_LOCAL_WHISPER") is not None
model = None
if SHOULD_RUN_LOCALLY:
    model = whisper.load_model("large")

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["audio"]
    if file is None:
        return jsonify({"result": "error", "message": "No file uploaded"})

    with tempfile.NamedTemporaryFile(delete=True, suffix=".webm") as tmp_file:
        file.save(tmp_file.name)
        if SHOULD_RUN_LOCALLY:
            text, lang = process_audio_locally(tmp_file)
        else:
            text, lang = process_audio_remote(tmp_file)

    text = make_journal(text, lang)
    return jsonify({"result": "success", "text": text})


def process_audio_locally(file):
    result = model.transcribe(file.name)
    return result["text"], result["language"]


def process_audio_remote(file):
    result = openai.Audio.transcribe("whisper-1", file, response_format="verbose_json")
    return result["text"], result["language"]


def make_journal(text, lang):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Given the following detailed account of events and actions from today, create a concise summary of the day in a Markdown list format. Distribute each item to one of the three categories: 'My Day', 'My Learnings' and open 'To-Dos'. To-dos should be displayed with a check box in front. The summary should exclude to-dos and learnings. In addition, based on the overall sentiment and tone of the text, determine the mood for the day and represent it with the word 'Mood' and a corresponding emoji in UTF-8 and no further text.\n\nWrite it in the following language: {lang}\nText: {text}",
            },
        ],
        max_tokens=1024,
    )

    return completion["choices"][0]["message"]["content"]


if __name__ == "__main__":
    app.run(debug=False)
