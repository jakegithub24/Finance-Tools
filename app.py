from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/emi_calculator', methods=['GET', 'POST'])
def emi_calculator():
    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            rate = float(request.form['rate'])
            tenure = float(request.form['tenure'])

            monthly_rate = rate / 12 / 100
            months = tenure * 12
            emi = principal * monthly_rate * \
                (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
            total_payment = emi * months
            total_interest = total_payment - principal

            return render_template('tools/emi_calculator.html',
                                   emi=round(emi, 2),
                                   total_payment=round(total_payment, 2),
                                   total_interest=round(total_interest, 2),
                                   calculated=True)
        except:
            return render_template('tools/emi_calculator.html', error=True)

    return render_template('tools/emi_calculator.html')


@app.route('/interest_calculator', methods=['GET', 'POST'])
def interest_calculator():
    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            rate = float(request.form['rate'])
            time = float(request.form['time'])

            simple_interest = (principal * rate * time) / 100
            amount = principal + simple_interest

            return render_template('tools/interest_calculator.html',
                                   simple_interest=round(simple_interest, 2),
                                   amount=round(amount, 2),
                                   calculated=True)
        except:
            return render_template('tools/interest_calculator.html', error=True)

    return render_template('tools/interest_calculator.html')


@app.route('/compound_interest', methods=['GET', 'POST'])
def compound_interest():
    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            rate = float(request.form['rate'])
            time = float(request.form['time'])
            compounding = int(request.form['compounding'])

            amount = principal * \
                (1 + rate/(100 * compounding)) ** (compounding * time)
            compound_interest = amount - principal

            return render_template('tools/compound_interest.html',
                                   compound_interest=round(
                                       compound_interest, 2),
                                   amount=round(amount, 2),
                                   calculated=True)
        except:
            return render_template('tools/compound_interest.html', error=True)

    return render_template('tools/compound_interest.html')


@app.route('/savings_goal', methods=['GET', 'POST'])
def savings_goal():
    if request.method == 'POST':
        try:
            goal_amount = float(request.form['goal_amount'])
            current_savings = float(request.form['current_savings'])
            monthly_contribution = float(request.form['monthly_contribution'])
            rate = float(request.form['rate'])

            monthly_rate = rate / 12 / 100
            remaining = goal_amount - current_savings
            months = 0
            balance = current_savings

            if monthly_contribution <= 0 and balance < goal_amount:
                return render_template('tools/savings_goal.html', error="Monthly contribution must be positive to reach your goal")

            while balance < goal_amount:
                balance *= (1 + monthly_rate)
                balance += monthly_contribution
                months += 1
                if months > 600:  # 50 years max
                    return render_template('tools/savings_goal.html', error="Goal not achievable with current parameters")

            years = months // 12
            remaining_months = months % 12

            return render_template('tools/savings_goal.html',
                                   years=years,
                                   months=remaining_months,
                                   total_months=months,
                                   calculated=True)
        except:
            return render_template('tools/savings_goal.html', error=True)

    return render_template('tools/savings_goal.html')


@app.route('/retirement_planning', methods=['GET', 'POST'])
def retirement_planning():
    if request.method == 'POST':
        try:
            current_age = int(request.form['current_age'])
            retirement_age = int(request.form['retirement_age'])
            current_savings = float(request.form['current_savings'])
            monthly_contribution = float(request.form['monthly_contribution'])
            rate = float(request.form['rate'])
            life_expectancy = int(request.form['life_expectancy'])

            years_to_retirement = retirement_age - current_age
            months_to_retirement = years_to_retirement * 12

            monthly_rate = rate / 12 / 100
            balance = current_savings

            # Calculate retirement savings
            for _ in range(months_to_retirement):
                balance *= (1 + monthly_rate)
                balance += monthly_contribution

            # Calculate monthly withdrawal during retirement
            retirement_years = life_expectancy - retirement_age
            retirement_months = retirement_years * 12
            retirement_monthly_rate = rate / 12 / 100

            monthly_withdrawal = balance * retirement_monthly_rate / \
                (1 - (1 + retirement_monthly_rate) ** (-retirement_months))

            return render_template('tools/retirement_planning.html',
                                   retirement_savings=round(balance, 2),
                                   monthly_withdrawal=round(
                                       monthly_withdrawal, 2),
                                   calculated=True)
        except:
            return render_template('tools/retirement_planning.html', error=True)

    return render_template('tools/retirement_planning.html')


@app.route('/currency_converter', methods=['GET', 'POST'])
def currency_converter():
    # Note: In a real application, you would use a currency API
    # For demonstration, we'll use fixed conversion rates
    conversion_rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.75, 'INR': 74.0, 'JPY': 110.0},
        'EUR': {'USD': 1.18, 'GBP': 0.88, 'INR': 87.0, 'JPY': 130.0},
        'GBP': {'USD': 1.33, 'EUR': 1.14, 'INR': 99.0, 'JPY': 150.0},
        'INR': {'USD': 0.014, 'EUR': 0.011, 'GBP': 0.010, 'JPY': 1.5},
        'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'GBP': 0.0067, 'INR': 0.67}
    }

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            from_currency = request.form['from_currency']
            to_currency = request.form['to_currency']

            if from_currency == to_currency:
                converted_amount = amount
            else:
                converted_amount = amount * \
                    conversion_rates[from_currency][to_currency]

            return render_template('tools/currency_converter.html',
                                   converted_amount=round(converted_amount, 2),
                                   calculated=True)
        except:
            return render_template('tools/currency_converter.html', error=True)

    return render_template('tools/currency_converter.html')


if __name__ == '__main__':
    app.run(debug=True, port=5500)
