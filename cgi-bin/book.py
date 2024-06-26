#!/usr/bin/env python3

import cgi
import cgitb

cgitb.enable()

print("Content-Type: text/html")
print()

# Predefined list of books with themes and prices (100 to 200 rupees range)
books = [
    {"title": "To Kill a Mockingbird", "price": 150, "theme": "Classic"},
    {"title": "1984", "price": 120, "theme": "Dystopian"},
    {"title": "Moby Dick", "price": 180, "theme": "Adventure"},
    {"title": "The Great Gatsby", "price": 170, "theme": "Classic"},
    {"title": "Brave New World", "price": 130, "theme": "Dystopian"},
    {"title": "The Hobbit", "price": 160, "theme": "Fantasy"},
    {"title": "Pride and Prejudice", "price": 110, "theme": "Romance"},
    {"title": "The Catcher in the Rye", "price": 140, "theme": "Classic"},
    {"title": "Fahrenheit 451", "price": 130, "theme": "Dystopian"},
    {"title": "Harry Potter", "price": 190, "theme": "Fantasy"},
]

# Get user input from form
form = cgi.FieldStorage()
theme = form.getvalue("theme")
price = float(form.getvalue("price"))
quantity = int(form.getvalue("quantity"))

# Filter books based on user preference
recommended_books = [
    book for book in books
    if book["theme"].lower() == theme.lower() and book["price"] <= price
]

print("<html>")
print("<head>")
print("<title>Book Recommendations</title>")
print("</head>")
print("<body>")
print("<h1>Recommended Books</h1>")

if recommended_books:
    print("<ul>")
    for book in recommended_books:
        print(f"<li>{book['title']} - ₹{book['price']:.2f} (Available Quantity: {quantity})</li>")
    print("</ul>")
else:
    print(f"<p>No books found for the theme '{theme}' within the price range ₹{price:.2f}</p>")

print("</body>")
print("</html>")
