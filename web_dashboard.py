from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Shared state file to store current readings
STATE_FILE = 'current_state.json'

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/current')
def get_current_data():
    """API endpoint to get current sensor readings"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                return jsonify(data)
        else:
            return jsonify({
                'co2': 0,
                'temperature': 0,
                'humidity': 0,
                'status': 'No Data',
                'warnings': [],
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🌐 Web Dashboard Starting...")
    print("=" * 60)
    print("\n📊 Access your dashboard at: http://localhost:5002")
    print("\n💡 Make sure main_csv.py is running in another terminal!")
    print("\n🛑 Press CTRL+C to stop the web server\n")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5002, use_reloader=False)
