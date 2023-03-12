# TXT to JPG

## Arguments
```
usage: txt_to_image_transfer.py [-h] [-p TEXTFILE_PATH] [--size SIZE] [--font FONT] [--max MAX] [--dark_mode]

optional arguments:
  -h, --help            show this help message and exit
  -p TEXTFILE_PATH, --textfile_path TEXTFILE_PATH
                        path to the text file to convert
  --size SIZE, --font_size SIZE
                        font size
  --font FONT, --font_path FONT
                        path to the font file
  --max MAX, --max_line_number MAX
                        max line number
  --dark_mode           dark mode
```

## Simple Usage
```
python3 txt_to_image_transfer.py -p <text_file_path>
```

## Output
```
./output/<text_file_name>
```