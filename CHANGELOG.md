# Changelog

## 0.3.0

- Changed
  - `dump` now supports binary file objects instead of text file objects

## 0.2.2

- Added
  - `multiline_strings` keyword argument for enabling multi-line strings
- Changed
  - Style: Do not make multi-line strings by default because they don't support lossless round-tripping

## 0.2.1

- Changed
  - Style: Decide between multi-line and single line string solely based on if line breaks are present

## 0.2.0

- Added
  - `tomli_w.dump`
- Changed
  - Style: Format strings containing line breaks and that are longer than threshold value as multiline strings

## 0.1.0

- Added
  - `tomli_w.dumps`
