# ImageToBlink
Possibly the world's worst image encoder. Convert any image to a micropython program (tested on RPi Pico) that will use the onboard LED to blink hexidecimal image data via morse code.

## Usage
```
python encoder.py {path/to/your/image.png}
```
## Output

Produces a file named `main.py` that can be loaded directly onto your RPi Pico device. I use [Thonny](https://thonny.org/) to do this.
