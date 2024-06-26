#!/usr/bin/env python3

import cgi
import cgitb

cgitb.enable()

print("Content-Type: text/html")
print()

# HTML form for loan calculator
form = cgi.FieldStorage()

# Retrieve form inputs
principal = form.getvalue('principal', '')
rate = form.getvalue('rate', '')
years = form.getvalue('years', '')

# Initialize variables
monthly_payment = 0.0

# Check if principal, rate, and years are provided and valid
if principal and rate and years:
    try:
        principal = float(principal)
        rate = float(rate) / 100.0
        years = int(years)
        if years > 0 and rate >= 0:  # Ensure years is positive and rate is non-negative
            # Calculate monthly payment
            monthly_rate = rate / 12
            months = years * 12
            if monthly_rate > 0:
                monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
            else:
                monthly_payment = principal / months
    except ValueError:
        print("<html>")
        print("<head><title>Loan Calculator Error</title></head>")
        print("<body>")
        print("<h1>Loan Calculator Error</h1>")
        print("<p>Please enter valid numeric values for loan amount, interest rate, and loan term.</p>")
        print("</body>")
        print("</html>")
        exit()

# Display results
print("<html>")
print("<head><title>Loan Calculator</title></head>")
print("<body>")
print("<h1>Loan Calculator</h1>")
print("<form>")
print("<label>Loan Amount ($): <input type='number' name='principal' value='{}'></label><br>".format(principal))
print("<label>Annual Interest Rate (%): <input type='number' name='rate' step='0.01' value='{}'></label><br>".format(rate * 100))
print("<label>Loan Term (years): <input type='number' name='years' value='{}'></label><br>".format(years))
print("<input type='submit' value='Calculate Monthly Payment'>")
print("</form>")
if monthly_payment > 0:
    print("<p>Monthly Payment: ${:.2f}</p>".format(monthly_payment))
print("</body>")
print("</html>")
