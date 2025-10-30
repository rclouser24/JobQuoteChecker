"""
Quote analyzer using Claude's vision API to extract information from quote images.
"""

import os
import base64
import re
import anthropic
from typing import List, Dict

def get_image_media_type(filename):
    """Determine the media type based on file extension"""
    ext = filename.lower().split('.')[-1]
    media_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return media_types.get(ext, 'image/jpeg')

def analyze_quote_image(image_data: bytes, filename: str) -> str:
    """
    Analyze a quote image using Claude's vision API.

    Args:
        image_data: Binary image data
        filename: Name of the file (used to determine media type)

    Returns:
        str: Analysis result from Claude
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    client = anthropic.Anthropic(api_key=api_key)

    # Encode image to base64
    image_base64 = base64.standard_b64encode(image_data).decode('utf-8')
    media_type = get_image_media_type(filename)

    # Create the message with vision
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": """Please analyze this home repair or remodeling quote image. Extract the following information:

1. List each line item/service with its description and price
2. Identify the type of work (e.g., bathroom_remodel, kitchen_remodel, roof_replacement, hvac_replacement, window_replacement, flooring_hardwood, flooring_tile, flooring_carpet, interior_painting, exterior_painting, plumbing_pipe_repair, electrical_panel_upgrade, etc.)
3. Extract the total cost if shown

Format your response as follows for each item:
ITEM: [description]
TYPE: [job_type]
PRICE: [amount in dollars, numbers only]

If you can identify the general category of work, use these standard types:
- bathroom_remodel
- kitchen_remodel (or kitchen_remodel_major for extensive work)
- roof_replacement
- hvac_replacement
- window_replacement
- siding_replacement
- flooring_hardwood, flooring_tile, or flooring_carpet
- deck_construction
- fence_installation
- drywall_repair
- interior_painting or exterior_painting
- electrical_panel_upgrade
- plumbing_pipe_repair
- water_heater_installation
- garage_door_replacement
- countertop_installation
- cabinet_installation
- basement_finishing
- insulation_installation
- gutter_installation

If the work doesn't fit these categories, use a descriptive name in lowercase with underscores.

Example:
ITEM: Kitchen cabinet installation - 20 linear feet
TYPE: cabinet_installation
PRICE: 5000

ITEM: Granite countertops - 45 sq ft
TYPE: countertop_installation
PRICE: 3150
"""
                    }
                ],
            }
        ],
    )

    # Extract the text content from the response
    response_text = message.content[0].text

    return response_text

def parse_analysis_result(analysis_text: str) -> List[Dict]:
    """
    Parse the analysis result from Claude into structured data.

    Args:
        analysis_text: Text response from Claude

    Returns:
        List of dictionaries containing item information
    """
    items = []

    # Split by ITEM: markers
    item_blocks = re.split(r'\n(?=ITEM:)', analysis_text)

    for block in item_blocks:
        if not block.strip() or 'ITEM:' not in block:
            continue

        # Extract description
        item_match = re.search(r'ITEM:\s*(.+?)(?:\n|$)', block)
        type_match = re.search(r'TYPE:\s*(.+?)(?:\n|$)', block)
        price_match = re.search(r'PRICE:\s*\$?([0-9,]+(?:\.[0-9]{2})?)', block)

        if item_match and type_match and price_match:
            description = item_match.group(1).strip()
            job_type = type_match.group(1).strip().lower()
            price_str = price_match.group(1).replace(',', '')

            try:
                price = float(price_str)

                items.append({
                    'description': description,
                    'job_type': job_type,
                    'price': price
                })
            except ValueError:
                # Skip items where price can't be parsed
                continue

    return items
