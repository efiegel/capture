# Capture
## Setup
Audio transcription requires ffmpeg.
```
brew install ffmpeg
```

## Use
Separate terminals for syncing audio from Voice Memos and transcribing them:
```
python -m scripts.sync
python -m scripts.transcribe
```