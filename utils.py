from pathlib import Path


def write_to_txt(string: str) -> None:
  with Path('./output.txt').open('w', encoding='utf8') as output_file:
    output_file.write(string)
    print('Sessions written to file.')
