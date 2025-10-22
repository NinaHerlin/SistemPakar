// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Global variables
let symptoms = [];
let selectedSymptoms = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
async function initializeApp() {
    try {
        await loadSymptoms();
        console.log('Application initialized successfully');
    } catch (error) {
        console.error('Error initializing application:', error);
        showError('Error loading application data. Please check if the backend server is running.');
    }
}

// Load symptoms from API
async function loadSymptoms() {
    try {
        console.log('Starting to load symptoms...');
        console.log('API_BASE_URL:', API_BASE_URL);
        
        const response = await fetch(`${API_BASE_URL}/symptoms`);
        console.log('Response status:', response.status);
        console.log('Response ok:', response.ok);
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.success) {
            symptoms = data.data;
            console.log('Loaded symptoms:', symptoms.length);
            renderSymptoms();
        } else {
            throw new Error(data.error || 'Failed to load symptoms');
        }
    } catch (error) {
        console.error('Error loading symptoms:', error);
        showError('Error loading symptoms data. Check console for details.');
    }
}

// Remove loadRiskFactors function since it's no longer needed

// Render symptoms checkboxes
function renderSymptoms() {
    const container = document.getElementById('symptoms-container');
    container.innerHTML = '';
    
    symptoms.forEach(symptom => {
        const checkboxItem = createCheckboxItem(symptom, 'symptom');
        container.appendChild(checkboxItem);
    });
}

// Remove renderRiskFactors function since it's no longer needed

// Create checkbox item element
function createCheckboxItem(item, type) {
    const div = document.createElement('div');
    div.className = 'checkbox-item';
    div.onclick = () => toggleCheckbox(item.id, type);
    
    div.innerHTML = `
        <input type="checkbox" id="${type}-${item.id}" />
        <span class="checkmark"></span>
        <h4>${item.name}</h4>
        <p>${item.description}</p>
    `;
    
    return div;
}

// Toggle checkbox selection
function toggleCheckbox(id, type) {
    const checkbox = document.getElementById(`${type}-${id}`);
    const checkboxItem = checkbox.parentElement;
    
    checkbox.checked = !checkbox.checked;
    
    if (checkbox.checked) {
        checkboxItem.classList.add('selected');
        selectedSymptoms.push(id);
    } else {
        checkboxItem.classList.remove('selected');
        selectedSymptoms = selectedSymptoms.filter(s => s !== id);
    }
    
    // Update diagnose button state
    updateDiagnoseButton();
}

// Update diagnose button state
function updateDiagnoseButton() {
    const diagnoseBtn = document.getElementById('diagnose-btn');
    const hasSelection = selectedSymptoms.length > 0;
    
    diagnoseBtn.disabled = !hasSelection;
}

// Perform diagnosis
async function performDiagnosis() {
    if (selectedSymptoms.length === 0) {
        showError('Silakan pilih setidaknya satu gejala atau faktor risiko.');
        return;
    }
    
    // Show loading
    showLoading(true);
    hideResults();
    
    try {
        const response = await fetch(`${API_BASE_URL}/diagnose`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symptoms: selectedSymptoms,
                risk_factors: [] // Empty since all are treated as symptoms in new system
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data.data);
        } else {
            throw new Error(data.error || 'Diagnosis failed');
        }
    } catch (error) {
        console.error('Error performing diagnosis:', error);
        showError('Error performing diagnosis. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Show loading indicator
function showLoading(show) {
    const loading = document.getElementById('loading');
    const diagnoseBtn = document.getElementById('diagnose-btn');
    
    if (show) {
        loading.style.display = 'block';
        diagnoseBtn.disabled = true;
    } else {
        loading.style.display = 'none';
        updateDiagnoseButton();
    }
}

// Show diagnosis results
function showResults(data) {
    const resultsSection = document.getElementById('results');
    const resultsContent = document.getElementById('results-content');
    const resultsPlaceholder = document.getElementById('results-placeholder');
    
    resultsContent.innerHTML = '';
    
    // Hide placeholder and show results
    if (resultsPlaceholder) {
        resultsPlaceholder.style.display = 'none';
    }
    
    if (data.diagnosis && data.diagnosis.length > 0) {
        // Show diagnosis results (now only highest confidence)
        data.diagnosis.forEach((diagnosis, index) => {
            const diagnosisElement = createDiagnosisElement(diagnosis, index + 1);
            resultsContent.appendChild(diagnosisElement);
        });
        
        // Show additional recommendations
        const additionalInfo = createAdditionalInfo();
        resultsContent.appendChild(additionalInfo);
    } else {
        const noDiagnosis = document.createElement('div');
        noDiagnosis.className = 'diagnosis-result';
        noDiagnosis.innerHTML = `
            <h3>Tidak Ditemukan Diagnosis</h3>
            <p>Berdasarkan gejala dan faktor risiko yang dipilih, tidak ditemukan diagnosis yang cocok. 
            Disarankan untuk tetap menjaga pola hidup sehat dan konsultasi dengan dokter jika ada keluhan.</p>
        `;
        resultsContent.appendChild(noDiagnosis);
    }
    
    resultsSection.style.display = 'block';
}

// Create diagnosis element
function createDiagnosisElement(diagnosis, index) {
    const div = document.createElement('div');
    div.className = 'diagnosis-result';
    
    const confidenceClass = getConfidenceClass(diagnosis.confidence);
    
    div.innerHTML = `
        <div class="diagnosis-header">
            <h3 class="diagnosis-title">${index}. ${diagnosis.disease_name}</h3>
            <span class="confidence-badge ${confidenceClass}">${diagnosis.confidence_percentage}%</span>
        </div>
        
        <p class="diagnosis-description">${diagnosis.description}</p>
        
        <div class="diagnosis-details">
            <p><strong>Tingkat Keparahan:</strong> ${diagnosis.severity}</p>
            <p><strong>Tingkat Kepercayaan:</strong> ${diagnosis.confidence_percentage}%</p>
            <p><strong>Rekomendasi:</strong> ${diagnosis.recommendation_level}</p>
        </div>
        
        <div class="recommendations">
            <h4>Saran Tindakan:</h4>
            <ul>
                ${diagnosis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>
    `;
    
    return div;
}

// Get confidence class for styling
function getConfidenceClass(confidence) {
    if (confidence >= 0.8) {
        return 'confidence-high';
    } else if (confidence >= 0.6) {
        return 'confidence-medium';
    } else {
        return 'confidence-low';
    }
}

// Create additional info element
function createAdditionalInfo() {
    const div = document.createElement('div');
    div.className = 'diagnosis-result';
    div.style.background = '#fff3cd';
    div.style.borderLeft = '4px solid #ffc107';
    
    div.innerHTML = `
        <h3><i class="fas fa-exclamation-triangle" style="color: #ffc107;"></i> Penting untuk Diketahui</h3>
        <p><strong>Perhatian:</strong> Hasil diagnosis ini hanya untuk skrining awal dan tidak menggantikan 
        diagnosis medis profesional. Selalu konsultasikan dengan dokter untuk diagnosis dan penanganan yang tepat.</p>
        
        <p><strong>Langkah selanjutnya:</strong></p>
        <ul>
            <li>Konsultasikan hasil ini dengan dokter</li>
            <li>Lakukan pemeriksaan medis yang disarankan</li>
            <li>Ikuti saran gaya hidup sehat</li>
            <li>Lakukan pemeriksaan rutin sesuai anjuran dokter</li>
        </ul>
    `;
    
    return div;
}

// Hide results
function hideResults() {
    const resultsSection = document.getElementById('results');
    const resultsPlaceholder = document.getElementById('results-placeholder');
    
    resultsSection.style.display = 'none';
    
    // Show placeholder again
    if (resultsPlaceholder) {
        resultsPlaceholder.style.display = 'flex';
    }
}

// Reset form
function resetForm() {
    // Clear selections
    selectedSymptoms = [];
    
    // Uncheck all checkboxes
    const checkboxes = document.querySelectorAll('.checkbox-item');
    checkboxes.forEach(item => {
        item.classList.remove('selected');
        const checkbox = item.querySelector('input[type="checkbox"]');
        checkbox.checked = false;
    });
    
    // Hide results
    hideResults();
    
    // Update button state
    updateDiagnoseButton();
}

// Show tab
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to selected tab button
    const selectedButton = event ? event.target : document.querySelector(`[onclick="showTab('${tabName}')"]`);
    if (selectedButton) {
        selectedButton.classList.add('active');
    }
}

// Show error message
function showError(message) {
    alert(message); // Simple alert for now, can be improved with custom modal
}

// Utility function to check API health
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.success) {
            console.log('API is healthy:', data);
            return true;
        } else {
            console.error('API health check failed:', data);
            return false;
        }
    } catch (error) {
        console.error('API health check error:', error);
        return false;
    }
}

// Check API health on page load
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(checkAPIHealth, 1000);
});