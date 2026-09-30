#!/usr/bin/python
import re
from pathlib import Path
import pymupdf
import pandas as pd
import argparse

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A command line tool designed to make text extraction from pdfs easier")
    parser.add_argument('target', type=Path, help="target directory or file")
    parser.add_argument('pattern', type=list[str], nargs="+", help="list of patterns to return as a table")

    return parser.parse_args()


def extract_pdf_contents(document_path:Path) -> str:
    with pymupdf.open(document_path) as doc:
        text = chr(12).join([page.get_text() for page in doc])
    return text

def get_matches(pdf_list:list[Path], match_criteria:list[str]) -> pd.DataFrame:
    """
    Given a list of pdfs, and a list of match criteria, this function returns a table with input docs as rows and match
    criteria as columns counting the number of matches
    """

    match_criteria = [r''.join(matches) for matches in match_criteria]
    data = []

    for pdf_path in pdf_list:
        extracted_text = extract_pdf_contents(Path(pdf_path))
        print(extracted_text)
        matches = [str(len(re.findall(criteria,extracted_text))) for criteria in match_criteria] # Get the number of matches
        new_row = [pdf_path.stem] + matches
        data.append(new_row)

    match_table = pd.DataFrame(data,columns=["PDF Name"] + match_criteria)
    return match_table

def execute_functionality(target_file:Path, match_criteria:list[str]):
    if not target_file.exists():
        raise ValueError("Path does not exist")
    if target_file.is_dir():
        path_list = [file for file in target_file.iterdir() if ".pdf" == file.suffix]
        matches = get_matches(path_list,match_criteria)
    elif target_file.suffix == ".pdf":
        matches = get_matches([target_file],match_criteria)
    else:
        raise ValueError("File is not a pdf or directory")

    print(matches)


if __name__ == '__main__':
    args = parse_arguments()
    execute_functionality(args.target,args.pattern)


