import json
import sys

def transcript_to_text(json_file, output_file):
    """Parses a JSON transcript file and outputs timestamps and text to a markdown file.

    Args:
        json_file (str): Path to the input JSON transcript file.
        output_file (str): Path to the output markdown file.
    """

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for segment in data['segments']:
            start_time = int(segment['start'])
            timestamp = f"**{start_time//3600:02d}:{(start_time//60)%60:02d}:{start_time%60:02d}**"
            text = segment['text'].strip()
            outfile.write(f"{timestamp} {text}\n\n")  # Add two line breaks for a paragraph break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <input_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace(".json", ".md")

    transcript_to_text(input_file, output_file)
