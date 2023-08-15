from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

def fetch_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except requests.exceptions.Timeout:
        pass  # Ignore timeout errors
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
    
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    merged_numbers = []

    start_time = time.time()

    for url in urls:
        if time.time() - start_time > 0.5:
            break  # Respect the 500ms timeout
        numbers = fetch_numbers_from_url(url)
        merged_numbers.extend(numbers)
    
    merged_numbers = list(set(merged_numbers))  # Remove duplicates
    merged_numbers.sort()  # Sort in ascending order
    
    return jsonify({"numbers": merged_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
