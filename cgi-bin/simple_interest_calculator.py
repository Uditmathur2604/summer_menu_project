#!/usr/bin/env python3

import cgi
import cgitb

cgitb.enable()

print("Content-Type: text/html")
print()

# HTML form for simple interest calculator
form = cgi.FieldStorage()

# Retrieve form inputs
principal = float(form.getvalue('principal', 0))
rate = float(form.getvalue('rate', 0))
years = int(form.getvalue('years', 0))

# Calculate simple interest
interest = (principal * rate * years) / 100
total_amount = principal + interest

# Display results
print("<html>")
print("<head><title>Simple Interest Calculator</title></head>")
print("<body>")
print("<h1>Simple Interest Calculator</h1>")
print("<form>")
print("<label>Principal Amount ($): <input type='number' name='principal' value='{}'></label><br>".format(principal))
print("<label>Rate of Interest (% per year): <input type='number' name='rate' step='0.01' value='{}'></label><br>".format(rate))
print("<label>Time Period (years): <input type='number' name='years' value='{}'></label><br>".format(years))
print("<input type='submit' value='Calculate Interest'>")
print("</form>")
print("<p>Interest Amount: ${:.2f}</p>".format(interest))
print("<p>Total Amount: ${:.2f}</p>".format(total_amount))
print("</body>")
print("</html>")
