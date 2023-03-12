from math import ceil

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)
import sys
import argparse
import os

PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1
FILE_OUTPUT_PATH = './output/'

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--textfile_path', type=str, help='path to the text file to convert')
parser.add_argument('--size', '--font_size', type=int, help='font size', default=20)
parser.add_argument('--font', '--font_path', type=str, help='path to the font file', default='./msjh.ttf')
parser.add_argument('--max', '--max_line_number', type=int, help='max line number', default=30)
parser.add_argument('--dark_mode', action='store_true', help='dark mode')

args = parser.parse_args()

def main():
    images = textfile_to_image(args.textfile_path)

    save_path = FILE_OUTPUT_PATH + args.textfile_path.split('/')[-1].split('.')[0] + '/'
    dark_mode_str = 'dark_mode-' if args.dark_mode else ''
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    for i, image in enumerate(images):
        image.save(save_path + dark_mode_str + str(i) + '.jpg')


def textfile_to_image(textfile_path):
    """Convert text file to a grayscale image.

    arguments:
    textfile_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """

    result = []

    # parse the file into lines stripped of whitespace on the right side
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())

    prev = object()
    lines = [prev:=v for v in lines if prev!=v]

    # choose a font (you can see more detail in the linked library on github)
    font = None
    font_filename = args.font
    try:
        font = ImageFont.truetype(font_filename, size=args.size)
        print(f'Using font "{font_filename}".')
    except IOError:
        print(f'Could not load font "{font_filename}".')

    # make a sufficiently sized background image based on the combination of font and lines
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 40

    # height of the background image
    max_line_number = args.max
    tallest_line = max(lines, key=lambda line: font.getsize(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(font.getsize(tallest_line)[PIL_HEIGHT_INDEX])
    realistic_line_height = max_line_height * 0.8  # apparently it measures a lot of space above visible content
    image_height = int(ceil(realistic_line_height * max_line_number + 2 * margin_pixels))

    # width of the background image
    widest_line = max(lines, key=lambda s: font.getsize(s)[PIL_WIDTH_INDEX])
    max_line_width = font_points_to_pixels(font.getsize(widest_line)[PIL_WIDTH_INDEX])
    max_line_width = int( ceil( max_line_width / 2 ) )
    image_width = int( ceil(max_line_width + (2 * margin_pixels)) )

    # split too long line
    new_lines = []
    line_max_number = int( ceil( max_line_width / args.size ) ) - 1
    for line in lines:
        if len(line) > line_max_number:
            new_lines.append( line[:line_max_number] )
            new_lines.append( line[line_max_number:] )
        else:
            new_lines.append( line )

    # draw the background
    background_color = 255 if args.dark_mode == False else 0
    result.append( Image.new(PIL_GRAYSCALE, (image_width, image_height), color=background_color) )
    draw = ImageDraw.Draw(result[0])

    # draw each line of text
    font_color = 0 if args.dark_mode == False else 255 
    horizontal_position = margin_pixels
    image_file_counter = 0
    line_counter = 0
    for line in new_lines:
        if line_counter >= max_line_number :
            line_counter = 0
            image_file_counter += 1
            result.append( Image.new(PIL_GRAYSCALE, (image_width, image_height), color=background_color) )
            draw = ImageDraw.Draw( result[ image_file_counter ] )
        
        vertical_position = int( round( margin_pixels + line_counter * realistic_line_height ) )

        if ( line_counter == 0 or line_counter == max_line_number - 1 ) and line == '' :
            continue
        
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font, anchor='lb')
        line_counter += 1

    return result
    

if __name__ == '__main__':
    main()
