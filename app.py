import os
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import anthropic
from utils.pricing_data import get_location_multiplier, AVERAGE_PRICES
from utils.quote_analyzer import analyze_quote_image, parse_analysis_result

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_quote():
    try:
        # Check if image file is present
        if 'quote_image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['quote_image']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, or PDF'}), 400

        # Get location data
        state = request.form.get('state', '').strip()
        city = request.form.get('city', '').strip()

        # Read and encode image
        image_data = file.read()

        # Analyze the quote image using Claude
        analysis_text = analyze_quote_image(image_data, file.filename)

        # Parse the analysis result
        quote_items = parse_analysis_result(analysis_text)

        # Calculate location multiplier
        location_multiplier = get_location_multiplier(state, city)

        # Compare with average prices and adjust for location
        results = []
        total_quoted = 0
        total_expected = 0

        for item in quote_items:
            job_type = item['job_type']
            quoted_price = item['price']

            # Get base average price
            base_average = AVERAGE_PRICES.get(job_type, {}).get('average', None)

            if base_average:
                # Adjust for location
                adjusted_average = base_average * location_multiplier
                adjusted_low = AVERAGE_PRICES[job_type]['low'] * location_multiplier
                adjusted_high = AVERAGE_PRICES[job_type]['high'] * location_multiplier

                # Determine if quote is above, below, or average
                if quoted_price < adjusted_low:
                    status = 'below'
                    message = 'Below average - good deal!'
                elif quoted_price > adjusted_high:
                    status = 'above'
                    message = 'Above average - consider negotiating'
                else:
                    status = 'average'
                    message = 'Within average range'

                difference = quoted_price - adjusted_average
                percent_diff = (difference / adjusted_average) * 100

                results.append({
                    'description': item['description'],
                    'job_type': job_type,
                    'quoted_price': quoted_price,
                    'average_price': round(adjusted_average, 2),
                    'price_range': {
                        'low': round(adjusted_low, 2),
                        'high': round(adjusted_high, 2)
                    },
                    'status': status,
                    'message': message,
                    'difference': round(difference, 2),
                    'percent_difference': round(percent_diff, 1)
                })

                total_quoted += quoted_price
                total_expected += adjusted_average
            else:
                results.append({
                    'description': item['description'],
                    'job_type': job_type,
                    'quoted_price': quoted_price,
                    'average_price': None,
                    'status': 'unknown',
                    'message': 'No pricing data available for this type of work'
                })
                total_quoted += quoted_price

        # Overall assessment
        if total_expected > 0:
            overall_diff = ((total_quoted - total_expected) / total_expected) * 100
            if overall_diff < -10:
                overall_status = 'excellent'
                overall_message = 'Great deal! This quote is significantly below average.'
            elif overall_diff < 5:
                overall_status = 'good'
                overall_message = 'Fair quote! Prices are reasonable.'
            elif overall_diff < 15:
                overall_status = 'average'
                overall_message = 'Slightly above average, but acceptable.'
            else:
                overall_status = 'high'
                overall_message = 'This quote is significantly above average. Consider getting other quotes.'
        else:
            overall_diff = 0
            overall_status = 'unknown'
            overall_message = 'Unable to determine pricing comparison.'

        return jsonify({
            'success': True,
            'location': {
                'city': city,
                'state': state,
                'multiplier': location_multiplier
            },
            'items': results,
            'summary': {
                'total_quoted': round(total_quoted, 2),
                'total_expected': round(total_expected, 2) if total_expected > 0 else None,
                'total_difference': round(total_quoted - total_expected, 2) if total_expected > 0 else None,
                'percent_difference': round(overall_diff, 1),
                'status': overall_status,
                'message': overall_message
            }
        })

    except Exception as e:
        app.logger.error(f"Error analyzing quote: {str(e)}")
        return jsonify({'error': f'Error analyzing quote: {str(e)}'}), 500

@app.route('/api/job-types', methods=['GET'])
def get_job_types():
    """Return list of supported job types"""
    job_types = list(AVERAGE_PRICES.keys())
    return jsonify({'job_types': job_types})

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
