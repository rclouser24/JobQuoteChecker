# Home Repair Quote Analyzer

A web application that analyzes home repair and remodeling quotes by comparing them against market averages and adjusting for your location. Upload a picture of your quote and get instant feedback on whether you're getting a fair deal!

## Features

- **AI-Powered Quote Analysis**: Uses Claude's vision API to extract information from quote images
- **Location-Based Pricing**: Adjusts pricing comparisons based on your state and city
- **Comprehensive Comparisons**: Compares quotes against national averages for 25+ common home repair jobs
- **Detailed Breakdowns**: See line-by-line analysis of each item in your quote
- **Beautiful Interface**: Clean, modern UI with intuitive upload and results display

## Supported Job Types

The analyzer includes pricing data for:
- Bathroom & Kitchen Remodels
- Roof Replacement
- HVAC Systems
- Window & Door Replacement
- Flooring (Hardwood, Tile, Carpet)
- Painting (Interior & Exterior)
- Plumbing & Electrical Work
- Countertops & Cabinets
- Decks & Fencing
- And many more...

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (for Claude vision API)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/JobQuoteChecker.git
cd JobQuoteChecker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# You can get an API key from: https://console.anthropic.com/
```

Example `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload a quote:
   - Click the upload area or drag and drop an image
   - Supported formats: PNG, JPG, JPEG, PDF
   - Optionally select your state and city for location-adjusted pricing

4. Click "Analyze Quote" and wait for the results

5. Review the analysis:
   - Overall quote assessment
   - Total cost comparison
   - Line-by-line breakdown with pricing status
   - Recommendations

## How It Works

1. **Image Upload**: You upload a picture of your home repair quote
2. **AI Extraction**: Claude's vision API analyzes the image and extracts:
   - Line items and descriptions
   - Prices for each item
   - Type of work being performed
3. **Price Comparison**: The app compares extracted prices against national averages
4. **Location Adjustment**: Prices are adjusted based on your location's cost of living
5. **Results**: You get a detailed breakdown showing if each item is above, below, or at market rate

## Location-Based Pricing

The app includes cost multipliers for major cities and states:

**High-Cost Areas** (1.3x - 1.7x):
- San Francisco, New York City, Boston, Seattle

**Average-Cost Areas** (0.95x - 1.15x):
- Denver, Austin, Chicago, Portland

**Low-Cost Areas** (0.85x - 0.95x):
- Texas (most cities), Ohio, Michigan, Arizona

## API Endpoints

### `POST /api/analyze`
Analyzes a quote image and returns pricing comparison.

**Request**:
- `quote_image` (file): Image file of the quote
- `state` (string, optional): Two-letter state code
- `city` (string, optional): City name

**Response**:
```json
{
  "success": true,
  "location": {
    "city": "Austin",
    "state": "TX",
    "multiplier": 1.10
  },
  "items": [
    {
      "description": "Kitchen cabinet installation",
      "job_type": "cabinet_installation",
      "quoted_price": 5000,
      "average_price": 5500,
      "price_range": { "low": 2200, "high": 11000 },
      "status": "below",
      "message": "Below average - good deal!",
      "difference": -500,
      "percent_difference": -9.1
    }
  ],
  "summary": {
    "total_quoted": 15000,
    "total_expected": 16500,
    "total_difference": -1500,
    "percent_difference": -9.1,
    "status": "excellent",
    "message": "Great deal! This quote is significantly below average."
  }
}
```

### `GET /api/job-types`
Returns list of supported job types.

## Project Structure

```
JobQuoteChecker/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore file
├── README.md             # This file
├── uploads/              # Temporary upload directory
├── utils/
│   ├── __init__.py
│   ├── pricing_data.py   # Pricing database and location multipliers
│   └── quote_analyzer.py # AI quote analysis logic
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── templates/
    └── index.html        # Main HTML template
```

## Customization

### Adding New Job Types

Edit `utils/pricing_data.py` and add entries to the `AVERAGE_PRICES` dictionary:

```python
AVERAGE_PRICES = {
    'your_job_type': {
        'low': 1000,
        'average': 2000,
        'high': 3000,
        'description': 'Description of the job'
    },
    # ... other entries
}
```

### Adding New Locations

Edit `utils/pricing_data.py` and add entries to the `LOCATION_MULTIPLIERS` dictionary:

```python
LOCATION_MULTIPLIERS = {
    'ST': {  # State code
        'default': 1.0,
        'cities': {
            'City Name': 1.2,
        }
    },
}
```

## Troubleshooting

**Error: "ANTHROPIC_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- Verify the key is valid and has available credits

**Quote not being analyzed correctly**
- Ensure the image is clear and text is readable
- Try uploading a higher quality image
- Make sure the quote format is standard (line items with prices)

**Location not found**
- Check that you're using the two-letter state code (e.g., 'CA', 'NY')
- If your city isn't in the database, the state average will be used
- You can add your city to `utils/pricing_data.py`

## Security Notes

- Never commit your `.env` file with real API keys
- The app stores uploaded files temporarily in the `uploads/` directory
- Consider implementing file cleanup for production use
- Add authentication if deploying publicly

## Future Enhancements

- [ ] User accounts and quote history
- [ ] PDF quote generation with analysis
- [ ] More job types and pricing data
- [ ] Additional location coverage
- [ ] Mobile app version
- [ ] Multi-contractor quote comparison
- [ ] Integration with contractor databases

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

Pricing data is based on national averages and may vary significantly based on:
- Specific materials chosen
- Scope of work
- Contractor experience
- Local market conditions
- Time of year

Always get multiple quotes and verify contractor credentials before proceeding with any home repair work.
