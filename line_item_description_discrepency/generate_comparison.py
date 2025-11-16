#!/usr/bin/env python3
"""
Generate a comparison PNG showing golden invoice descriptions vs modified invoice descriptions
with similarity scores.
"""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

def load_invoice(filepath):
    """Load and return invoice JSON data."""
    with open(filepath, 'r') as f:
        return json.load(f)

def calculate_similarity(text1, text2):
    """
    Calculate a simple similarity score based on word overlap.
    Returns a percentage (0-100).
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 and not words2:
        return 100.0
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    # Jaccard similarity
    similarity = len(intersection) / len(union) if union else 0.0
    return similarity * 100

def get_all_descriptions():
    """Extract all descriptions from golden and modified invoices."""
    base_dir = Path(__file__).parent
    golden_dir = base_dir.parent / "golden_invoices"
    
    comparisons = []
    
    # Get all modified invoices (without '_')
    modified_files = sorted(base_dir.glob("invoice_*.json"))
    modified_files = [f for f in modified_files if not f.name.startswith('_')]
    
    for modified_file in modified_files:
        # Find corresponding golden invoice
        golden_file = golden_dir / modified_file.name
        
        if not golden_file.exists():
            continue
        
        golden_invoice = load_invoice(golden_file)
        modified_invoice = load_invoice(modified_file)
        
        # Match line items by item_id
        golden_items = {item['item_id']: item for item in golden_invoice.get('line_items', [])}
        modified_items = {item['item_id']: item for item in modified_invoice.get('line_items', [])}
        
        # Compare matching items
        for item_id in golden_items:
            if item_id in modified_items:
                golden_desc = golden_items[item_id]['description']
                modified_desc = modified_items[item_id]['description']
                similarity = calculate_similarity(golden_desc, modified_desc)
                
                comparisons.append({
                    'golden': golden_desc,
                    'modified': modified_desc,
                    'similarity': similarity
                })
    
    return comparisons

def create_comparison_image(comparisons, output_path):
    """Create a PNG image with the comparison table."""
    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
        header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 12)
            header_font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()
    
    # Create a temporary draw object to measure text
    temp_img = Image.new('RGB', (100, 100), color='white')
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Calculate column widths based on actual text width
    headers = ["Golden Invoice Description", "Modified Invoice Description", "Similarity Score"]
    
    # Measure header widths
    header_widths = []
    for header in headers:
        bbox = temp_draw.textbbox((0, 0), header, font=header_font)
        header_widths.append(bbox[2] - bbox[0])
    
    # Measure content widths
    golden_widths = []
    modified_widths = []
    similarity_widths = []
    
    for comp in comparisons:
        # Golden description
        bbox = temp_draw.textbbox((0, 0), comp['golden'], font=font)
        golden_widths.append(bbox[2] - bbox[0])
        
        # Modified description
        bbox = temp_draw.textbbox((0, 0), comp['modified'], font=font)
        modified_widths.append(bbox[2] - bbox[0])
        
        # Similarity score
        similarity_text = f"{comp['similarity']:.2f}%"
        bbox = temp_draw.textbbox((0, 0), similarity_text, font=font)
        similarity_widths.append(bbox[2] - bbox[0])
    
    # Calculate column widths (max of header and content, plus small padding)
    cell_padding = 8  # Horizontal padding in cells
    col_widths = [
        max(max(golden_widths) if golden_widths else 0, header_widths[0]) + cell_padding,
        max(max(modified_widths) if modified_widths else 0, header_widths[1]) + cell_padding,
        max(max(similarity_widths) if similarity_widths else 0, header_widths[2]) + cell_padding
    ]
    
    # Image dimensions - minimized margins
    margin = 20
    cell_padding_vertical = 4  # Top and bottom padding in cells
    row_height = 28  # Reduced row height
    header_height = 32  # Reduced header height
    
    width = sum(col_widths) + margin * 2
    height = header_height + len(comparisons) * row_height + margin * 2
    
    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw header
    y = margin
    x = margin
    for i, header in enumerate(headers):
        draw.rectangle([x, y, x + col_widths[i], y + header_height], 
                      fill='#4A90E2', outline='black', width=1)
        # Center text
        bbox = draw.textbbox((0, 0), header, font=header_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((x + (col_widths[i] - text_width) // 2, 
                  y + (header_height - text_height) // 2),
                 header, fill='white', font=header_font)
        x += col_widths[i]
    
    # Draw rows
    y = margin + header_height
    for comp in comparisons:
        x = margin
        row_data = [
            comp['golden'],
            comp['modified'],
            f"{comp['similarity']:.2f}%"
        ]
        
        for i, text in enumerate(row_data):
            # Draw cell background
            fill_color = '#F5F5F5' if y % (row_height * 2) == margin + header_height else 'white'
            draw.rectangle([x, y, x + col_widths[i], y + row_height],
                          fill=fill_color, outline='black', width=1)
            
            # Draw text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_height = bbox[3] - bbox[1]
            
            draw.text((x + cell_padding // 2, y + (row_height - text_height) // 2),
                     text, fill='black', font=font)
            
            x += col_widths[i]
        
        y += row_height
    
    # Save image
    img.save(output_path)
    print(f"Comparison image saved to {output_path}")

def main():
    base_dir = Path(__file__).parent
    output_path = base_dir / "description_discrepancy_comparison.png"
    
    print("Extracting descriptions from invoices...")
    comparisons = get_all_descriptions()
    
    print(f"Found {len(comparisons)} line item comparisons")
    print("Generating comparison image...")
    create_comparison_image(comparisons, output_path)
    
    print("Done!")

if __name__ == "__main__":
    main()

