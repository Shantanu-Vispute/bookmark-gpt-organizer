import pandas as pd
from openai import OpenAI
import time
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def create_classification_prompt(bookmark: Dict) -> str:
    category_structure = """
    Categories:
    1. DSA
        ├── Blogs
        ├── Tutorials
        └── Resources

    2. Mobile Development
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    3. UI Libraries

    4. UI Inspiration
        ├── General
        └── Aggregators

    5. Icon Libraries

    6. AI
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    7. Frontend
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    8. Backend
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    9. Databases
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    10. Cloud
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    11. General
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    12. System Design
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    13. Career
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Job Platforms

    14. Boilerplate/Starter Kits

    15. News Aggregators

    16. General JS
        ├── Blogs
        ├── Tutorials
        ├── Resources
        └── Tools

    17. Community
        └── Profiles (e.g. LinkedIn, X, Github, etc.)

    18. Uncategorized (Anything that doesn't fit into the other categories, but first try to find a category that is close, then if it doesn't fit into any category, then it is Uncategorized)
    """

    prompt = f"""Please analyze the following bookmark and suggest an appropriate hierarchical category path based on the provided category structure.

Category Structure:
{category_structure}

Consider the content, purpose, and target audience of the resource.

Title: {bookmark['title']}
Excerpt: {bookmark['excerpt']}
URL: {bookmark['url']}

Suggest a category path in the format "Main Category / Subcategory" that best describes this resource.
If the bookmark does not fit into any of the predefined categories, assign it to "Others".
Return only the category path without any additional text or explanation.
"""

    return prompt


def get_category_from_openai(bookmark: Dict) -> str:
    try:
        response = client.chat.completions.create( 
            model=os.getenv("MODEL_NAME"),
            messages=[
                {"role": "system", "content": "You are a bookmark categorization assistant. Analyze the content and suggest an appropriate hierarchical category. Respond only with the category path in the format 'Main Category / Subcategory'."},
                {"role": "user", "content": create_classification_prompt(bookmark)}
            ],
            temperature=0.2,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting category for bookmark {bookmark['title']}: {str(e)}")
        return "Uncategorized"

def process_bookmarks(input_file: str, output_file: str):
    try:
        input_df = pd.read_csv(input_file)
        unique_categories = set()
        
        if 'folder' not in input_df.columns:
            input_df['folder'] = None
        
        processed_urls = set()
        if os.path.exists(output_file):
            output_df = pd.read_csv(output_file)
            processed_urls = set(output_df['url'].tolist())
            unique_categories = set(output_df['folder'].tolist())
        else:
            input_df.iloc[0:0].to_csv(output_file, index=False)
        
        remaining_df = input_df[~input_df['url'].isin(processed_urls)]
        
        if len(remaining_df) == 0:
            print("All bookmarks have already been processed!")
            return
        
        print(f"Processing {len(remaining_df)} remaining bookmarks...")
        
        for index, row in remaining_df.iterrows():
            print(f"Processing bookmark {index + 1}/{len(remaining_df)}: {row['title']}")
            
            bookmark = {
                'title': row['title'],
                'excerpt': row['excerpt'] if pd.notna(row['excerpt']) else '',
                'url': row['url']
            }
            
            category = get_category_from_openai(bookmark)
            unique_categories.add(category)
            
            new_row = row.copy()
            new_row['folder'] = category
            
            new_row.to_frame().T.to_csv(output_file, mode='a', header=False, index=False)
            
            print(f"Categorized as: {category}")
            print("Row written to output file")
            print("-" * 50)
            
            time.sleep(1)
        
        print(f"\nCategorization complete. Results saved to {output_file}")
        
        final_df = pd.read_csv(output_file)
        
        print("\nCategory Distribution:")
        print(final_df['folder'].value_counts())
        
        print("\nUnique Categories Generated:")
        for category in sorted(unique_categories):
            print(f"- {category}")
        
    except Exception as e:
        print(f"Error processing bookmarks: {str(e)}")

def main():
    input_file = os.getenv("INPUT_FILE")
    output_file = os.getenv("OUTPUT_FILE")
    
    process_bookmarks(input_file, output_file)

if __name__ == "__main__":
    main()