// DOM Elements
const quoteForm = document.getElementById('quoteForm');
const quoteImageInput = document.getElementById('quoteImage');
const fileUploadBox = document.getElementById('fileUploadBox');
const filePreview = document.getElementById('filePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('results');
const errorDiv = document.getElementById('error');

// File upload handling
quoteImageInput.addEventListener('change', handleFileSelect);

// Drag and drop
fileUploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadBox.classList.add('drag-over');
});

fileUploadBox.addEventListener('dragleave', () => {
    fileUploadBox.classList.remove('drag-over');
});

fileUploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadBox.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        quoteImageInput.files = files;
        handleFileSelect();
    }
});

function handleFileSelect() {
    const file = quoteImageInput.files[0];

    if (file) {
        // Show preview
        filePreview.innerHTML = '';

        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                filePreview.appendChild(img);

                const fileName = document.createElement('p');
                fileName.textContent = file.name;
                filePreview.appendChild(fileName);
            };
            reader.readAsDataURL(file);
        } else {
            const fileName = document.createElement('p');
            fileName.textContent = `Selected: ${file.name}`;
            filePreview.appendChild(fileName);
        }
    }
}

// Form submission
quoteForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Hide previous results/errors
    resultsSection.style.display = 'none';
    errorDiv.style.display = 'none';

    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.querySelector('.btn-text').style.display = 'none';
    analyzeBtn.querySelector('.btn-loader').style.display = 'inline';

    try {
        const formData = new FormData(quoteForm);

        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze quote');
        }

        // Display results
        displayResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').style.display = 'inline';
        analyzeBtn.querySelector('.btn-loader').style.display = 'none';
    }
});

function displayResults(data) {
    // Show results section
    resultsSection.style.display = 'block';

    // Location info
    const locationInfo = document.getElementById('locationInfo');
    if (data.location.state) {
        locationInfo.innerHTML = `
            <strong>Location:</strong> ${data.location.city ? data.location.city + ', ' : ''}${data.location.state}
            <br>
            <strong>Regional Cost Multiplier:</strong> ${data.location.multiplier.toFixed(2)}x
            ${data.location.multiplier > 1 ? '(Higher than national average)' : data.location.multiplier < 1 ? '(Lower than national average)' : '(National average)'}
        `;
    } else {
        locationInfo.innerHTML = `
            <strong>Location:</strong> Using national average pricing (no location specified)
        `;
    }

    // Summary card
    const summaryCard = document.getElementById('summaryCard');
    const summary = data.summary;

    let statusClass = 'status-' + summary.status;
    let statusText = summary.status.toUpperCase();

    summaryCard.innerHTML = `
        <h3>Overall Quote Assessment</h3>
        <p style="font-size: 1.1rem; margin-bottom: 8px;">${summary.message}</p>
        <span class="status-badge ${statusClass}">${statusText}</span>

        <div class="price-comparison">
            <div class="price-item">
                <label>Total Quoted</label>
                <div class="value">$${summary.total_quoted.toLocaleString()}</div>
            </div>
            ${summary.total_expected ? `
                <div class="price-item">
                    <label>Expected Average</label>
                    <div class="value">$${summary.total_expected.toLocaleString()}</div>
                </div>
                <div class="price-item">
                    <label>Difference</label>
                    <div class="value" style="color: ${summary.total_difference > 0 ? '#fc8181' : '#68d391'}">
                        ${summary.total_difference > 0 ? '+' : ''}$${summary.total_difference.toLocaleString()}
                        (${summary.percent_difference > 0 ? '+' : ''}${summary.percent_difference}%)
                    </div>
                </div>
            ` : ''}
        </div>
    `;

    // Items breakdown
    const itemsBreakdown = document.getElementById('itemsBreakdown');
    itemsBreakdown.innerHTML = '<h3>Line Item Analysis</h3>';

    data.items.forEach(item => {
        const itemCard = document.createElement('div');
        itemCard.className = `item-card status-${item.status}`;

        let statusBadge = '';
        if (item.status !== 'unknown') {
            statusBadge = `<span class="item-status ${item.status}">${item.status.toUpperCase()}</span>`;
        } else {
            statusBadge = `<span class="item-status unknown">NO DATA</span>`;
        }

        let detailsHTML = '';
        if (item.average_price !== null && item.average_price !== undefined) {
            detailsHTML = `
                <div class="item-details">
                    <div class="detail-item">
                        <label>Quoted Price</label>
                        <div class="value">$${item.quoted_price.toLocaleString()}</div>
                    </div>
                    <div class="detail-item">
                        <label>Average Price</label>
                        <div class="value">$${item.average_price.toLocaleString()}</div>
                    </div>
                    <div class="detail-item">
                        <label>Price Range</label>
                        <div class="value" style="font-size: 1rem;">
                            $${item.price_range.low.toLocaleString()} - $${item.price_range.high.toLocaleString()}
                        </div>
                    </div>
                    <div class="detail-item">
                        <label>Difference</label>
                        <div class="value ${item.difference > 0 ? 'negative' : 'positive'}">
                            ${item.difference > 0 ? '+' : ''}$${item.difference.toLocaleString()}
                            (${item.percent_difference > 0 ? '+' : ''}${item.percent_difference}%)
                        </div>
                    </div>
                </div>
                <p style="margin-top: 12px; color: #4a5568; font-weight: 500;">${item.message}</p>
            `;
        } else {
            detailsHTML = `
                <div class="item-details">
                    <div class="detail-item">
                        <label>Quoted Price</label>
                        <div class="value">$${item.quoted_price.toLocaleString()}</div>
                    </div>
                </div>
                <p style="margin-top: 12px; color: #4a5568; font-weight: 500;">${item.message}</p>
            `;
        }

        itemCard.innerHTML = `
            <div class="item-header">
                <div class="item-description">
                    <h4>${item.description}</h4>
                    <p class="job-type">${item.job_type.replace(/_/g, ' ')}</p>
                </div>
                ${statusBadge}
            </div>
            ${detailsHTML}
        `;

        itemsBreakdown.appendChild(itemCard);
    });

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}
