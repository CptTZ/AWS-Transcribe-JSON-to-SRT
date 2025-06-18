import json
import re
import codecs
import time
import math
import os
import argparse

def newPhrase():
    return { 'start_time': '', 'end_time': '', 'words' : [] }

def getTimeCode(seconds):
    (frac, whole) = math.modf(seconds)
    frac = frac * 1000
    return str('%s,%03d' % (time.strftime('%H:%M:%S',time.gmtime(whole)), frac))

def writeTranscriptToSRT(transcript, sourceLangCode, srtFileName):
    print("==> Creating SRT from transcript")
    phrases = getPhrasesFromTranscript(transcript)
    writeSRT(phrases, srtFileName)

def getPhrasesFromTranscript(transcript):
    ts = json.loads(transcript)
    items = ts['results']['items']

    phrase = newPhrase()
    phrases = []
    nPhrase = True
    x = 0
    c = 0
    lastEndTime = ""

    print("==> Creating phrases from transcript...")

    for item in items:
        if nPhrase == True:
            if item["type"] == "pronunciation":
                phrase["start_time"] = getTimeCode(float(item["start_time"]))
                nPhrase = False
                lastEndTime = getTimeCode(float(item["end_time"]))
            c += 1
        else:
            if item["type"] == "pronunciation":
                phrase["end_time"] = getTimeCode(float(item["end_time"]))
                lastEndTime = phrase["end_time"]

        phrase["words"].append(item['alternatives'][0]["content"])
        x += 1

        if x == 10:
            phrases.append(phrase)
            phrase = newPhrase()
            nPhrase = True
            x = 0

    if len(phrase["words"]) > 0:
        if phrase['end_time'] == '':
            phrase['end_time'] = lastEndTime
        phrases.append(phrase)

    return phrases

def writeSRT(phrases, filename):
    print("==> Writing phrases to disk...")

    e = codecs.open(filename, "w+", "utf-8")
    x = 1

    for phrase in phrases:
        length = len(phrase["words"])

        e.write(str(x) + "\n")
        x += 1

        e.write(phrase["start_time"] + " --> " + phrase["end_time"] + "\n")

        out = getPhraseText(phrase)

        e.write(out + "\n\n")

    e.close()
    print(f"==> SRT file successfully written to {filename}")

def getPhraseText(phrase):
    length = len(phrase["words"])

    out = ""
    for i in range(0, length):
        if re.match('[a-zA-Z0-9]', phrase["words"][i]):
            if i > 0:
                out += " " + phrase["words"][i]
            else:
                out += phrase["words"][i]
        else:
            out += phrase["words"][i]

    return out

def main():
    parser = argparse.ArgumentParser(description='Convert JSON transcription to SRT file')
    parser.add_argument('input_file', help='Path to input JSON file')
    parser.add_argument('-o', '--output', help='Path to output SRT file (default: same name as input with .srt extension)')

    args = parser.parse_args()

    input_file = args.input_file

    # If no output file is specified, use the input filename with .srt extension
    if args.output:
        output_file = args.output
    else:
        output_file = os.path.splitext(input_file)[0] + ".srt"

    print(f"==> Reading JSON file: {input_file}")
    print(f"==> Output will be written to: {output_file}")

    try:
        with open(input_file, "r") as f:
            json_content = f.read()
            writeTranscriptToSRT(json_content, 'en', output_file)
            print("==> Conversion completed successfully")
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {input_file}")
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON format in input file")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()
