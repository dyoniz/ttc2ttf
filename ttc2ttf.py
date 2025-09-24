import argparse
import os
import sys
import tempfile
import fontforge
from fontTools.ttLib import TTCollection


FONT_FAMILY_NAME_ID = 1
FONT_SUBFAMILY_NAME_ID = 2
FONT_FULL_NAME_ID = 4


def fontforge_generate(input_path, out_path):
    font = fontforge.open(input_path)
    font.generate(out_path)


def get_font_name(font, name_id):
    name_table = font["name"]
    for name in name_table.names:
        if name.nameID != name_id:
            continue
        try:
            return name.string.decode(name.getEncoding())
        except Exception:
            return name.string.decode(errors="replace")
    return ""


def get_family_name(font):
    return get_font_name(font, name_id=FONT_FAMILY_NAME_ID)


def get_full_name(font):
    return get_font_name(font, name_id=FONT_FULL_NAME_ID)


def get_subfamily(font):
    return get_font_name(font, name_id=FONT_SUBFAMILY_NAME_ID)


def get_font_filename(font):
    family_name = get_family_name(font)
    subfamily = get_subfamily(font)
    if subfamily:
        subfamily = subfamily.replace(" ", "")
    if not family_name:
        return subfamily
    if not subfamily:
        return family_name
    return f"{family_name}_{subfamily}"


def main():
    if len(sys.argv) == 1:
        print("Usage: python ttc2ttf.py <ttc_file> [--monospaced] [--output-folder <output_folder>]")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Converts ttc fonts to ttf.")
    parser.add_argument("--monospaced", action="store_true", help="Monospaced font")
    parser.add_argument(
        "--output-folder",
        dest="output_folder",
        default=".",
        help="Output folder for generated ttf files (default: current directory)",
    )
    parser.add_argument("input_file", help="Input file")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: input file '{args.input_file}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.output_folder):
        try:
            os.makedirs(args.output_folder, exist_ok=True)
            print(f"Created output folder: {args.output_folder}")
        except Exception as e:
            print(
                f"Error: could not create output folder '{args.output_folder}': {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    print(f"Monospaced: {args.monospaced}")
    print(f"Input file: {args.input_file}")
    print(f"Output folder: {args.output_folder}")

    base_name = os.path.splitext(args.input_file)[0]

    font_collection = TTCollection(args.input_file)

    used_filenames = set()

    for i, font in enumerate(font_collection.fonts):
        print(f"Font {i} Full name: {get_full_name(font)}")
        print(f"Font {i} Family name: {get_family_name(font)}")
        print(f"Font {i} Subfamily name: {get_subfamily(font)}")
        print(
            f"Font {i} Subfamily name (joined): {get_subfamily(font).replace(' ', '')}"
        )
        if args.monospaced and "post" in font:
            font["post"].isFixedPitch = True
        with tempfile.NamedTemporaryFile(suffix=".ttf", delete=True) as tmp_ttf:
            font.save(tmp_ttf.name)
            filename = get_font_filename(font)
            if not filename or filename in used_filenames:
                filename = f"{base_name}_{i}"
            used_filenames.add(filename)
            out_path = os.path.join(args.output_folder, f"{filename}.ttf")
            fontforge_generate(tmp_ttf.name, out_path)


if __name__ == "__main__":
    main()
