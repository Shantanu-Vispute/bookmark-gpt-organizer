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

## Customization

The categorization structure is fully customizable. Modify the `category_structure` in `create_classification_prompt()` to match your preferences:

```python
category_structure = """
Categories:
1. Your Category
    ├── Subcategory 1
    ├── Subcategory 2
    └── Subcategory 3

2. Another Category
    ├── Custom Subcategory
    └── More Subcategories
"""
```

## Setup

1. Clone repository
2. Install dependencies:
3. Add OpenAI API key to `.env`
4. Place bookmark CSV in root as `bookmarks.csv`

## Usage

```bash
python categorize.py
```
