# JournalGPT

_This is just a proof of concept (PoC), not a fully developed product. However, it serves as an idea for combining text-to-speech and LLMs (Large Language Models)._

Are you tired of writing long journal entries every day? Are you also tired of reading them in the future? Let's simplify things by using text-to-speech technology to dictate your daily experiences. The LLM (GPT-3.5 Turbo) will create a summary and categorize it for you in these categories:

- Your day
- Learnings
- To-dos

## Prerequisites

Before running this project, you need to have the following installed on your system:

- `Python 3`
- `pip`

## Installation

To install the project dependencies, run the following command:

`pip install -r requirements.txt`

## Usage

`OPENAI_API_KEY=<your-api-key> python app.py`

This will start a web server at http://localhost:5000. Click on `Record` to begin dictating your daily experiences. Once you're done, click 'Stop' and wait for the input to be processed.

## Mobile Usage

To use it in Safari on iOS, you need to access it via `HTTP_S_`. The simplest way is to use [ngrok](https://ngrok.com/).
Simply install and sign up for ngrok, then run `ngrok http 5000`.

## Text to Speech

We're utilizing the [Whisper ASR](https://openai.com/research/whisper) (Automatic Speech Recognition) system developed by OpenAI. You have two options: running it locally by setting the environment variable `USE_LOCAL_WHISPER=1` or using OpenAI's Whisper API, which is the default and faster. When running locally, the large model (approximately 2-3 GB) will be downloaded and the TTS will be processed on your machine.