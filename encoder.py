from pathlib import Path
from PIL import Image
import argparse

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}


BLINK_HEADER = f'''
from machine import Pin
import time
led=Pin(25, Pin.OUT)
d={MORSE_CODE_DICT}
'''


def get_args():

    parser = argparse.ArgumentParser(description='Convert images to blink micropython blink instructions.')
    parser.add_argument('image', help='Path to image to convert')
    
    return parser.parse_args()


def add_image_hex_to_header(hex_string):
    header = BLINK_HEADER + f'\nimage_hex="{hex_string}"'
    return header


def display_morse_string():

    return '''
def display_morse(image_hex):

    def get_time_on(dot_or_dash):
        if dot_or_dash == '-':
            time_on = 0.6
        else:
            time_on = 0.3
        return time_on

    for each_char in image_hex:
        morse = d[each_char.upper()]
        for each_symbol in morse:
            time_on = get_time_on(each_symbol)
            led.toggle()
            time.sleep(time_on)
            led.toggle()
            time.sleep(0.3)
        time.sleep(1)

display_morse(image_hex)
    '''


def resize_image(image_path):
    image_path = Path(image_path)
    image = Image.open(str(image_path))
    image = image.resize((128, 128))
    small_image_path = image_path.with_suffix(f'.small.{image_path.suffix}')
    image.save(str(small_image_path))
    return small_image_path


def convert_image_to_hex(image_path):
    with open(str(image_path), 'rb') as handle:
        return handle.read().hex()


def write_main(hex_string):
    header = add_image_hex_to_header(hex_string)
    with open('main.py', 'w') as handle:
        handle.write(header)
        handle.write(display_morse_string())


def main():
    args = get_args()
    image = args.image
    small_image = resize_image(image)
    hex_string = convert_image_to_hex(small_image)
    write_main(hex_string)

if __name__ == '__main__':
    main()


