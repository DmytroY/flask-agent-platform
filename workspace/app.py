from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version": "1.0.0"})

if __name__ == '__main__':
    app.run(debug=True)