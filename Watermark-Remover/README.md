# PDF Watermark Remover 

A powerful, efficient, and user-friendly Python tool to remove tiled watermarks and promotional footer text from PDF question papers.

## Features

- **Smart Detection**: Automatically identifies large tiled watermarks and specific promotional keywords in PDF content streams.
- **Recursive Processing**: Handles deeply nested folder structures (e.g., `jee/year-wise/2021/...`) with ease.
- **GUI Folder Picker**: No command-line hassle! Simply run the script to open a visual folder selection dialog.
- **Progress Tracking**: Real-time progress bar using `tqdm` shows you exactly how many files are left.
- **Safe Cleaning**: Non-destructive removal. It "blanks" watermark objects while preserving the PDF's structural integrity (BBox/Matrix), ensuring the files remain valid and printable.
- **Hierarchy Preservation**: Creates a parallel `_Cleaned` folder that mirrors your original directory structure exactly.
- **Detailed Summary**: Provides a report of Total Scanned, Modified, and Skipped files at the end of every run.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Watermark-Remover.git
   cd Watermark-Remover
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Simple GUI Mode (Recommended)
Just run the script, and a folder picker window will appear:
```bash
python remove_watermark.py
```

### Option 2: CLI Mode
Specify the input folder (or file) and optionally the output location:
```bash
# Process a folder
python remove_watermark.py "path/to/Enstine Notes"

# Process a single file
python remove_watermark.py input.pdf output.pdf
```

## How it Works

The script leverages the `pikepdf` library to inspect the underlying PDF structure. 

1. **Identification**: It looks for `Form XObjects`. Objects larger than 50KB are usually the tiled logo background. Smaller objects are scanned for keywords like `mathongo`, `links.mathongo`, etc.
2. **Blanking**: Instead of deleting the objects (which can cause layout shifts or errors), it replaces their content stream with an empty one.
3. **Preservation**: It copies all necessary metadata (BBox, Matrix) to ensure the PDF viewer treats the "empty" object as if it's still there, but renders nothing.

## Dependencies

- `pikepdf`: High-performance PDF manipulation.
- `tqdm`: Fast, extensible progress bars.
- `tkinter`: Standard Python GUI library (for folder selection).

---
*Disclaimer: This tool is for personal use and educational purposes only. Please respect the copyrights of the original content creators.*
