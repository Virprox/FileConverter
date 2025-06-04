#file_converter.py
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="File Converter: Convert files between different formats.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file")
    parser.add_argument("-f", "--format", required=True, help="Target format for conversion (e.g., csv, json)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Target format: {args.format}")

if __name__ == "__main__":
    main()