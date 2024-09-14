# Capture
## Setup
Audio transcription requires ffmpeg.
```
brew install ffmpeg
```

### Environment
Create an `.env` file and assign values for the following:
```
AUDIO_DIRECTORY=
OPENAI_API_KEY=
VAULT_DIRECTORY=
```

## Using scripts
To add text to your vault via command line:
```
python -m scripts.capture
```

To transcribe and add audio content to your vault:
```
python -m scripts.listen
```
