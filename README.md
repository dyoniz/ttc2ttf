# ttc2ttf

Convert TTC font to TTF.

`ttc2ttf.py` is a simple Python script, that takes single TTC file as an input and produces bunch of TTF files as an output, one TTF file for each font stored in TTC file.

## Installation

### On MacOS

```bash
brew install fontforge
pip install fonttools
```

## Usage

```text
python ttc2ttf.py <ttc_file> [--monospaced] [--output-folder <output_folder>]
```

Use `--monospaced` option for fixed sized fonts.

If `--output-folder` is ommited, TTF files will be saved into current location.

## Usage Example

```bash
python ttc2ttf.py bin/Courier.ttc --monospaced --output-folder bin/Courier

cp bin/Courier/*.ttf ~/Library/Fonts
```
