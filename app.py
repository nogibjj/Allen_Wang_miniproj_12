import os
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv

app = Flask(__name__)

# Serve the homepage
@app.route('/')
def home():
    return "Databricks File Checker and Image Display API"

# Endpoint to check file status
@app.route('/check-file', methods=['POST'])
def check_file():
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    url = f"https://{server_h}/api/2.0"

    data = request.json
    file_path = data.get("file_path")

    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = request.get(url + f"/dbfs/get-status?path={file_path}", headers=headers)
        response.raise_for_status()
        return jsonify({"file_exists": True, "file_path": file_path})
    except Exception as e:
        return jsonify({"file_exists": False, "error": str(e)})

# Endpoint to serve the image
@app.route('/display-image', methods=['GET'])
def display_image():
    image_path = "mylib/top_10_countries_alcohol_consumption.png"  # Adjust as per your Docker file structure
    full_path = os.path.join("/Workspace/Shared/Allen_Wang_miniproj_11", image_path)

    if os.path.exists(full_path):
        return send_file(full_path, mimetype='image/png')
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
