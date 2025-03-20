from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.Crawler import Crawler

app = Flask(__name__)
CORS(app)

@app.post('/crawler')
def set_up_crawler():
    config = request.get_json()
    if not config:
        return jsonify({"error": "Invalid or missing config"}), 400

    try:
        crawler = Crawler(config)
        print(config)
        start_url = config.get("TargetURL", "https://example.com")
        response = "<html></html>"
        crawler.processResponse(start_url, f"GET {start_url}", response)

        return jsonify(crawler.tree_creator.return_data())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
