from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Flask App!'

@app.route('/run_script', methods=['POST'])
def run_script():
    # Get the URL from the request data
    url = request.json.get('url')
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
