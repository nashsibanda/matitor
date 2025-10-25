# Matitorge

**Matitor** is a *Mat*roska Sub*tit*le Extract*or* and M*er*ger with additional tools for merging subtitles.

Forked from [0x64746b's original Matitor project](https://github.com/0x64746b/matitor).

## Features

- Extract subtitles from Matroska (.mkv) files
- Merge multiple subtitle files (ASS/SSA/SRT) into a single file
- Batch process directories of video files
- File dialogs for interactive use
- Support for ASS, SSA, SRT, and other subtitle formats

## File Naming Requirements

**Batch processing** requires specific file naming conventions:

- MKV files: `*.mkv`
- Subtitle files must start with the same name as the MKV file
- Only one subtitle file per MKV file is allowed
- Supported subtitle extensions: `.srt`, `.ass`, `.ssa`, `.sub`, `.json`, `.txt`, `.vtt`, `.sami`, `.smi`, `.ttml`

Example:

```text
movie.mkv
movie.ja.ass          # ✓ Valid
other_movie.ass    # ✗ Invalid (different stem)
movie.srt          # ✗ Invalid (multiple files)
```

**Output files** are saved with the same name as the input MKV file.

## Installation

### Prerequisites

- Python 3.13 or higher
- `mkvtoolnix` (for the original matitor.py functionality)

### Setup

1. Clone the repository:

```shell
git clone <repository-url>
cd matitor
```

1. Install dependencies:

```shell
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Usage

### Main Interface (run.py)

```shell
$ python run.py -h
usage: run.py [-h] {extract,merge,full,batch,batch-cli} ...

The command to run

positional arguments:
  {extract,merge,full,batch,batch-cli}
    extract             The command to run
    merge               The command to run
    full                The command to run
    batch               The command to run
    batch-cli           The command to run

options:
  -h, --help            show this help message and exit
```

#### Available Commands

- **`extract`**: Extract subtitles from an MKV file
- **`merge`**: Merge two subtitle files
- **`full`**: Extract from MKV and merge with additional subtitles
- **`batch`**: Batch process a directory of MKV files
- **`batch-cli`**: Batch process a directory from command line

#### Examples

**Extract subtitles:**

```shell
$ python run.py extract
# Opens file dialog to select MKV file
```

**Merge subtitle files:**

```shell
$ python run.py merge
# Opens file dialogs to select original and additional subtitle files
```

**Extract and merge:**

```shell
$ python run.py full
# Opens file dialogs to select MKV file and additional subtitle file
```

**Batch process directory:**

```shell
$ python run.py batch
# Opens directory dialog to select folder containing MKV files
```

**Batch process from command line:**

```shell
$ python run.py batch-cli --directory-path /path/to/videos
# Processes all MKV files in the specified directory
```

### Command Line Interface (matitor.py)

The original command-line interface:

```shell
$ python matitor.py -h
usage: matitor.py [-h] mkv_file

Extract subtitles from a Matroska file.

positional arguments:
  mkv_file    the .mkv to extract an .srt from

optional arguments:
  -h, --help  show this help message and exit
```

**Example:**

```shell
$ python matitor.py my_summer_holidays.mkv
ID: 2 - Lang: eng - Track Name: Foreign Speaking Parts Only - Codec: S_TEXT/UTF8
ID: 3 - Lang: eng - Track Name: - Codec: S_TEXT/UTF8
Please enter the ID of the track to be extracted: 2
Selected track: ID: 2 - Lang: eng - Track Name: Foreign Speaking Parts Only - Codec: S_TEXT/UTF8
```

## Dependencies

### Runtime Dependencies

- **pymkv2** (>=2.1.2): Modern Python wrapper for MKVToolNix, used for subtitle extraction
- **pysubs2** (>=1.8.0): Python library for reading and writing subtitle files (ASS, SSA, SRT, etc.)

### Development Dependencies

- **mypy** (>=1.18.2): Static type checker for Python
- **ruff** (>=0.14.2): Fast Python linter and formatter

### System Dependencies

- **mkvtoolnix**: Required for the `matitor.py` interface
  - Install via package manager (e.g., `brew install mkvtoolnix` on macOS)
  - Or download from [MKVToolNix website](https://mkvtoolnix.download/)

## Project Structure

- **`matitor.py`**: Original command-line subtitle extractor
- **`run.py`**: Main entry point with multiple commands
- **`subs_merge/`**: Core processing modules
  - **`extractor.py`**: Subtitle extraction using pymkv2
  - **`merger.py`**: Subtitle file merging
  - **`batch.py`**: Batch processing
  - **`full_process.py`**: Extract and merge workflow
  - **`gui.py`**: File dialogs for interactive use
