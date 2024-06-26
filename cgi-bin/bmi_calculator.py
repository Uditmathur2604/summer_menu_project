#!/usr/bin/env python3

import cgi
import cgitb

cgitb.enable()

print("Content-Type: text/html")
print()

# HTML form for BMI calculator
form = cgi.FieldStorage()

# Retrieve form inputs
weight = form.getvalue('weight', '')
height = form.getvalue('height', '')

# Initialize variables
bmi = 0.0
bmi_category = ''

# Check if weight and height are provided and valid
if weight and height:
    try:
        weight = float(weight)
        height = float(height)
        if height > 0:  # Ensure height is positive to avoid division by zero
            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)
            # Determine BMI category
            if bmi < 18.5:
                bmi_category = 'Underweight'
            elif bmi < 24.9:
                bmi_category = 'Normal weight'
            elif bmi < 29.9:
                bmi_category = 'Overweight'
            else:
                bmi_category = 'Obese'
    except ValueError:
        print("<html>")
        print("<head><title>BMI Calculator Error</title></head>")
        print("<body>")
        print("<h1>BMI Calculator Error</h1>")
        print("<p>Please enter valid numeric values for weight and height.</p>")
        print("</body>")
        print("</html>")
        exit()

# Display results
print("<html>")
print("<head><title>BMI Calculator</title></head>")
print("<body>")
print("<h1>BMI Calculator</h1>")
print("<form>")
print("<label>Weight (kg): <input type='number' name='weight' value='{}'></label><br>".format(weight))
print("<label>Height (cm): <input type='number' name='height' value='{}'></label><br>".format(height))
print("<input type='submit' value='Calculate BMI'>")
print("</form>")
if bmi:
    print("<p>BMI: {:.2f}</p>".format(bmi))
    print("<p>Category: {}</p>".format(bmi_category))
print("</body>")
print("</html>")
