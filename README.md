# Bookmark GPT Organizer

Transform unstructured bookmarks into hierarchically organized collections using GPT.

## Features

- Processes CSV exports from bookmark managers
- GPT-4 powered content analysis and categorization
- Hierarchical category structure
- Resume-capable processing
- Progress tracking

## Requirements

Input CSV must contain the following columns:

- `title`: The bookmark title
- `url`: The bookmark URL
- `excerpt`: A description or excerpt of the bookmark content

## Setup

1. Clone repository
2. Install dependencies:
3. Add OpenAI API key to `.env`
4. Place bookmark CSV in root as `bookmarks.csv`

## Usage

```bash
python categorize.py
```
