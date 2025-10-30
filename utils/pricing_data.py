"""
Pricing data for common home repair and remodeling jobs.
Prices are national averages in USD and include labor and materials.
"""

# Average pricing data for common home repairs and remodels
AVERAGE_PRICES = {
    'bathroom_remodel': {
        'low': 6000,
        'average': 10500,
        'high': 15000,
        'description': 'Full bathroom remodel'
    },
    'kitchen_remodel': {
        'low': 12000,
        'average': 25000,
        'high': 35000,
        'description': 'Kitchen remodel (mid-range)'
    },
    'kitchen_remodel_major': {
        'low': 35000,
        'average': 65000,
        'high': 95000,
        'description': 'Major kitchen remodel'
    },
    'roof_replacement': {
        'low': 5500,
        'average': 8500,
        'high': 11500,
        'description': 'Roof replacement (asphalt shingles, 1,700 sq ft)'
    },
    'hvac_replacement': {
        'low': 5000,
        'average': 7500,
        'high': 10000,
        'description': 'HVAC system replacement'
    },
    'window_replacement': {
        'low': 450,
        'average': 650,
        'high': 850,
        'description': 'Window replacement (per window)'
    },
    'siding_replacement': {
        'low': 8000,
        'average': 12000,
        'high': 16000,
        'description': 'Vinyl siding replacement (1,500 sq ft)'
    },
    'flooring_hardwood': {
        'low': 8,
        'average': 12,
        'high': 18,
        'description': 'Hardwood flooring installation (per sq ft)'
    },
    'flooring_tile': {
        'low': 7,
        'average': 15,
        'high': 25,
        'description': 'Tile flooring installation (per sq ft)'
    },
    'flooring_carpet': {
        'low': 3,
        'average': 7,
        'high': 12,
        'description': 'Carpet installation (per sq ft)'
    },
    'deck_construction': {
        'low': 4000,
        'average': 7500,
        'high': 11000,
        'description': 'Deck construction (wood, 200 sq ft)'
    },
    'fence_installation': {
        'low': 13,
        'average': 27,
        'high': 40,
        'description': 'Fence installation (per linear foot)'
    },
    'drywall_repair': {
        'low': 75,
        'average': 200,
        'high': 350,
        'description': 'Drywall repair (small to medium hole)'
    },
    'interior_painting': {
        'low': 2,
        'average': 4,
        'high': 6,
        'description': 'Interior painting (per sq ft)'
    },
    'exterior_painting': {
        'low': 1.50,
        'average': 3.50,
        'high': 5.50,
        'description': 'Exterior painting (per sq ft)'
    },
    'electrical_panel_upgrade': {
        'low': 1500,
        'average': 2500,
        'high': 3500,
        'description': 'Electrical panel upgrade (200 amp)'
    },
    'plumbing_pipe_repair': {
        'low': 150,
        'average': 400,
        'high': 650,
        'description': 'Plumbing pipe repair'
    },
    'water_heater_installation': {
        'low': 800,
        'average': 1500,
        'high': 2200,
        'description': 'Water heater installation (tank)'
    },
    'garage_door_replacement': {
        'low': 750,
        'average': 1500,
        'high': 2500,
        'description': 'Garage door replacement (single door)'
    },
    'countertop_installation': {
        'low': 40,
        'average': 70,
        'high': 100,
        'description': 'Countertop installation (per sq ft, granite)'
    },
    'cabinet_installation': {
        'low': 100,
        'average': 250,
        'high': 500,
        'description': 'Cabinet installation (per linear foot)'
    },
    'basement_finishing': {
        'low': 25,
        'average': 50,
        'high': 75,
        'description': 'Basement finishing (per sq ft)'
    },
    'insulation_installation': {
        'low': 1.50,
        'average': 3,
        'high': 4.50,
        'description': 'Insulation installation (per sq ft)'
    },
    'gutter_installation': {
        'low': 4,
        'average': 8,
        'high': 12,
        'description': 'Gutter installation (per linear foot)'
    },
}

# Location-based cost of living multipliers
# These adjust pricing based on geographic location
LOCATION_MULTIPLIERS = {
    'CA': {
        'default': 1.35,
        'cities': {
            'San Francisco': 1.65,
            'Los Angeles': 1.45,
            'San Diego': 1.40,
            'San Jose': 1.60,
            'Oakland': 1.50,
        }
    },
    'NY': {
        'default': 1.30,
        'cities': {
            'New York': 1.60,
            'Manhattan': 1.70,
            'Brooklyn': 1.55,
            'Queens': 1.45,
            'Buffalo': 1.10,
        }
    },
    'MA': {
        'default': 1.25,
        'cities': {
            'Boston': 1.45,
            'Cambridge': 1.50,
        }
    },
    'WA': {
        'default': 1.20,
        'cities': {
            'Seattle': 1.40,
            'Bellevue': 1.38,
        }
    },
    'CO': {
        'default': 1.15,
        'cities': {
            'Denver': 1.25,
            'Boulder': 1.30,
        }
    },
    'TX': {
        'default': 0.95,
        'cities': {
            'Austin': 1.10,
            'Houston': 0.95,
            'Dallas': 1.00,
            'San Antonio': 0.90,
        }
    },
    'FL': {
        'default': 0.98,
        'cities': {
            'Miami': 1.15,
            'Orlando': 0.95,
            'Tampa': 0.93,
        }
    },
    'IL': {
        'default': 1.05,
        'cities': {
            'Chicago': 1.25,
        }
    },
    'AZ': {
        'default': 0.95,
        'cities': {
            'Phoenix': 0.98,
            'Scottsdale': 1.10,
        }
    },
    'NC': {
        'default': 0.92,
        'cities': {
            'Charlotte': 1.00,
            'Raleigh': 0.98,
        }
    },
    'GA': {
        'default': 0.93,
        'cities': {
            'Atlanta': 1.05,
        }
    },
    'OR': {
        'default': 1.10,
        'cities': {
            'Portland': 1.20,
        }
    },
    'NV': {
        'default': 0.95,
        'cities': {
            'Las Vegas': 0.98,
        }
    },
    'MI': {
        'default': 0.88,
        'cities': {
            'Detroit': 0.90,
        }
    },
    'OH': {
        'default': 0.87,
        'cities': {
            'Columbus': 0.92,
            'Cleveland': 0.88,
        }
    },
    'PA': {
        'default': 0.95,
        'cities': {
            'Philadelphia': 1.08,
            'Pittsburgh': 0.93,
        }
    },
}

def get_location_multiplier(state, city=None):
    """
    Get the location-based cost multiplier for a given state and city.

    Args:
        state: Two-letter state code (e.g., 'CA', 'NY')
        city: City name (optional)

    Returns:
        float: Cost multiplier (1.0 = national average)
    """
    if not state:
        return 1.0

    state = state.upper().strip()

    if state not in LOCATION_MULTIPLIERS:
        # Unknown state, use national average
        return 1.0

    state_data = LOCATION_MULTIPLIERS[state]

    # Check if specific city is provided and has data
    if city:
        city = city.strip().title()
        if city in state_data.get('cities', {}):
            return state_data['cities'][city]

    # Return state default
    return state_data['default']

def get_all_states():
    """Return list of all states with pricing data"""
    return list(LOCATION_MULTIPLIERS.keys())

def get_cities_for_state(state):
    """Return list of cities with specific pricing data for a state"""
    state = state.upper().strip()
    if state in LOCATION_MULTIPLIERS:
        return list(LOCATION_MULTIPLIERS[state].get('cities', {}).keys())
    return []
