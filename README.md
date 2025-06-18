# Amazon Transcribe JSON to SRT

This is a Python script that converts Amazon Transcribe JSON output into a more readable and usable SRT file format.

This was created to allow Amazon Transcribe users to receive a more widely used format of their transcripts. The SRT output can be used to display the transcript as subtitles under a video or audio.

## How to use

### Command Line Usage

```
python transcript_to_srt.py input_file.json [-o output_file.srt]
```

#### Arguments:

- `input_file.json`: Path to the JSON file from Amazon Transcribe
- `-o, --output`: (Optional) Path to output SRT file. If not specified, uses the same name as input with .srt extension

#### Example:

python transcript_to_srt.py my_transcript.json -o my_subtitles.srt

If you don't specify an output file, the script will create an SRT file in the same location as the input file:

```
python transcript_to_srt.py my_transcript.json
```

## Features

- Formats transcripts into standard SRT subtitle format
- Handles timestamps and properly formats them for SRT compatibility
- Creates phrases of appropriate length for subtitles (10 words per subtitle)
- Preserves punctuation from the original transcription
