// Basic form validation
document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const inputs = this.querySelectorAll('input[required]');
            let valid = true;

            inputs.forEach(input => {
                if (!input.value || parseFloat(input.value) <= 0) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Please fill in all required fields with valid values');
            }
        });
    });

    // Clear validation on input
    const requiredInputs = document.querySelectorAll('input[required]');
    requiredInputs.forEach(input => {
        input.addEventListener('input', function () {
            if (this.value && parseFloat(this.value) > 0) {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Add real-time calculation for some tools
    if (document.getElementById('principal') && document.getElementById('rate') &&
        document.getElementById('tenure') && document.getElementById('emi_result')) {
        setupEMICalculator();
    }
});

// Real-time EMI calculator (optional enhancement)
function setupEMICalculator() {
    const principalInput = document.getElementById('principal');
    const rateInput = document.getElementById('rate');
    const tenureInput = document.getElementById('tenure');

    if (principalInput && rateInput && tenureInput) {
        const inputs = [principalInput, rateInput, tenureInput];

        inputs.forEach(input => {
            input.addEventListener('input', calculateEMI);
        });
    }
}

function calculateEMI() {
    const principal = parseFloat(document.getElementById('principal').value) || 0;
    const rate = parseFloat(document.getElementById('rate').value) || 0;
    const tenure = parseFloat(document.getElementById('tenure').value) || 0;

    if (principal > 0 && rate > 0 && tenure > 0) {
        const monthlyRate = rate / 12 / 100;
        const months = tenure * 12;
        const emi = principal * monthlyRate * (1 + monthlyRate) ** months / ((1 + monthlyRate) ** months - 1);
        const totalPayment = emi * months;
        const totalInterest = totalPayment - principal;

        document.getElementById('emi_result').textContent = emi.toFixed(2);
        document.getElementById('total_payment_result').textContent = totalPayment.toFixed(2);
        document.getElementById('total_interest_result').textContent = totalInterest.toFixed(2);
    }
}