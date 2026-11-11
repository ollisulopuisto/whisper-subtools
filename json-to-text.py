import json
import sys
from pathlib import Path

def transcript_to_text(json_file, output_file):
    """Parses a JSON transcript file and outputs timestamps and text to a markdown file.

    Args:
        json_file (str): Path to the input JSON transcript file.
        output_file (str): Path to the output markdown file.
    """

    source = Path(json_file)
    destination = Path(output_file)
    if source.resolve() == destination.resolve() or (
        destination.exists() and source.samefile(destination)
    ):
        raise ValueError("Output must be different from the input transcript")

    with source.open('r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for segment in data['segments']:
            start_time = int(segment['start'])
            timestamp = f"**{start_time//3600:02d}:{(start_time//60)%60:02d}:{start_time%60:02d}**"
            text = segment['text'].strip()
            outfile.write(f"{timestamp} {text}\n\n")  # Add two line breaks for a paragraph break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json-to-text.py <input_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = Path(input_file).with_suffix(".md")

    try:
        transcript_to_text(input_file, output_file)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
