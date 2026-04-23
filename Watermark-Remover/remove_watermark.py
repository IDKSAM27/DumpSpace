#!/usr/bin/env python3
"""
MathonGo Watermark Remover
--------------------------
Removes the "mathongo" tiled watermark and footer text from MathonGo PDF question papers.

Usage:
    # Single file
    python3 remove_watermark.py input.pdf

    # Single file with custom output
    python3 remove_watermark.py input.pdf output.pdf

    # All PDFs in a folder
    python3 remove_watermark.py /path/to/folder/

    # All PDFs in a folder, save to a different output folder
    python3 remove_watermark.py /path/to/folder/ /path/to/output/

How it works:
    MathonGo PDFs embed watermarks as PDF Form XObjects (Fm0, Fm1, etc.).
    This script identifies those XObjects and replaces their content with
    empty streams, making them render nothing while keeping the PDF valid.
"""

import sys
import argparse
from pathlib import Path
import pikepdf
from pikepdf import Pdf, Stream
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm


# ── Detection thresholds ──────────────────────────────────────────────────────
# Form XObjects larger than this (bytes) are treated as the logo watermark tile
LARGE_FORM_THRESHOLD = 50_000

# Keywords that identify a footer/promo watermark in small form XObjects
WATERMARK_KEYWORDS = [b"mathongo", b"MathonGo", b"links.mathongo", b"mWN"]


def is_watermark_xobject(obj: pikepdf.Object) -> bool:
    """Return True if this XObject is a MathonGo watermark."""
    # Must be a Form XObject
    subtype = obj.get("/Subtype")
    if subtype != pikepdf.Name("/Form"):
        return False

    try:
        raw = obj.read_bytes()
    except Exception:
        return False

    # Large form XObjects are the tiled logo watermark
    if len(raw) > LARGE_FORM_THRESHOLD:
        return True

    # Small form XObjects: check for mathongo keywords
    raw_lower = raw.lower()
    if any(kw.lower() in raw_lower for kw in WATERMARK_KEYWORDS):
        return True

    return False


def blank_xobject(obj: pikepdf.Object) -> None:
    """Replace an XObject's content stream with an empty one in-place."""
    # Preserve BBox and Matrix so the PDF structure stays valid
    bbox  = obj.get("/BBox",   pikepdf.Array([0, 0, 1, 1]))
    matrix = obj.get("/Matrix", pikepdf.Array([1, 0, 0, 1, 0, 0]))

    # Write an empty content stream
    obj.write(b"")  # empty stream body
    obj["/BBox"]    = bbox
    obj["/Matrix"]  = matrix
    obj["/Subtype"] = pikepdf.Name("/Form")
    obj["/Type"]    = pikepdf.Name("/XObject")

    # Remove optional keys that are no longer valid for an empty stream
    for key in ["/Resources", "/Group", "/Metadata", "/PieceInfo",
                "/LastModified", "/StructParents"]:
        if key in obj:
            del obj[key]


def remove_watermarks_from_pdf(input_path: Path, output_path: Path, verbose: bool = False) -> int:
    """
    Process one PDF file. Returns the number of watermark XObjects removed.
    """
    replaced = 0

    with Pdf.open(input_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            resources = page.obj.get("/Resources")
            if resources is None:
                continue
            xobjs = resources.get("/XObject")
            if xobjs is None:
                continue

            for name, obj in xobjs.items():
                try:
                    if is_watermark_xobject(obj):
                        blank_xobject(obj)
                        replaced += 1
                        if verbose:
                            print(f"  Page {page_num:>3}: blanked XObject {name}")
                except Exception as exc:
                    if verbose:
                        print(f"  Page {page_num}: WARNING – could not process {name}: {exc}")

        if replaced:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            pdf.save(output_path)

    return replaced


def process_file(input_path: Path, output_path: Path, verbose: bool = True) -> int:
    if verbose:
        print(f"\n{'─'*60}")
        print(f"Input : {input_path}")
        print(f"Output: {output_path}")
    n = remove_watermarks_from_pdf(input_path, output_path, verbose=verbose)
    if verbose and n:
        size_before = input_path.stat().st_size / 1024
        size_after  = output_path.stat().st_size / 1024
        print(f"  Done. {n} watermark object(s) removed.")
        print(f"  File size: {size_before:.0f} KB → {size_after:.0f} KB")
    return n


def select_folder(title="Select Folder"):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring to front
    folder_path = filedialog.askdirectory(title=title)
    root.destroy()
    return Path(folder_path) if folder_path else None


def main():
    parser = argparse.ArgumentParser(
        description="Remove MathonGo watermarks from PDF files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to a PDF file or a directory containing PDF files.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        help=(
            "Output PDF file (when input is a file) or output directory "
            "(when input is a directory). Defaults to <input>_Cleaned "
            "or <input_dir>_Cleaned/."
        ),
    )
    args = parser.parse_args()

    input_path = Path(args.input) if args.input else None

    # ── GUI Fallback ──────────────────────────────────────────────────────────
    if not input_path:
        print("No input provided. Opening folder selection dialog...")
        input_path = select_folder("Select the 'Enstine Notes' or any PDF folder")
        if not input_path:
            print("No folder selected. Exiting.")
            sys.exit(0)

    # ── Directory mode ────────────────────────────────────────────────────────
    if input_path.is_dir():
        pdf_files = sorted(input_path.glob("**/*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in {input_path}")
            sys.exit(1)

        out_dir = Path(args.output) if args.output else input_path.parent / f"{input_path.name}_Cleaned"
        print(f"Found {len(pdf_files)} PDF file(s) in {input_path}")
        print(f"Output directory: {out_dir}")
        print("\nProcessing...")

        stats = {"total": len(pdf_files), "modified": 0, "skipped": 0, "errors": 0}

        # Use tqdm for a nice progress bar
        with tqdm(pdf_files, desc="Cleaning PDFs", unit="file") as pbar:
            for pdf_file in pbar:
                # Update progress bar description with current file (short name)
                pbar.set_postfix(file=pdf_file.name[:20])

                # Preserve sub-directory structure inside out_dir
                rel = pdf_file.relative_to(input_path)
                out_file = out_dir / rel
                try:
                    # In bulk mode, we keep it quiet unless there's an error
                    n = remove_watermarks_from_pdf(pdf_file, out_file, verbose=False)
                    if n > 0:
                        stats["modified"] += 1
                    else:
                        stats["skipped"] += 1
                except Exception as exc:
                    stats["errors"] += 1
                    print(f"\n  ERROR processing {pdf_file.name}: {exc}")

        print(f"\n{'═'*60}")
        print(f"Batch Processing Complete!")
        print(f"  Total Scanned : {stats['total']}")
        print(f"  Modified      : {stats['modified']}")
        print(f"  Skipped       : {stats['skipped']}")
        if stats["errors"]:
            print(f"  Errors        : {stats['errors']}")
        print(f"Clean PDFs saved to: {out_dir}")

    # ── Single-file mode ──────────────────────────────────────────────────────
    elif input_path.is_file():
        if args.output:
            out_file = Path(args.output)
        else:
            out_file = input_path.with_stem(input_path.stem + "_Cleaned")

        process_file(input_path, out_file, verbose=True)

    else:
        print(f"Error: {input_path} is not a valid file or directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
