import os
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
import requests
from io import BytesIO
import json
import base64

app = Flask(__name__)

# Serve the homepage
@app.route('/')
def home():
    return "Databricks File Checker and Image Display API"

# Endpoint to check file status
@app.route('/check-file', methods=['GET'])
def check_file():
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    url = f"https://{server_h}/api/2.0"

    # Get file_path from query parameters
    file_path = request.args.get("file_path")

    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        response = requests.get(url + f"/dbfs/get-status?path={file_path}", headers=headers)
        response.raise_for_status()
        return jsonify({"file_exists": True, "file_path": file_path})
    except Exception as e:
        return jsonify({"file_exists": False, "error": str(e)})

@app.route('/display-image1', methods=['GET'])
def display_image1():
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    
    reqUrl = f"https://{server_h}/api/2.0/dbfs/read"
    
    headersList = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "path": "/FileStore/Allen_mini_project11/top_10_countries_alcohol_consumption.png"
    })

    try:
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        response.raise_for_status()
        
        image_data = base64.b64decode(response.json()['data'])
        
        return send_file(
            BytesIO(image_data),
            mimetype='image/png',
            as_attachment=False
        )

    except requests.exceptions.RequestException as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response is not None:
            error_detail = e.response.text

        return jsonify({
            "error": "Request failed",
            "message": str(e),
            "details": error_detail
        }), 404

@app.route('/display-image2', methods=['GET'])
def display_imag2():
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    
    reqUrl = f"https://{server_h}/api/2.0/dbfs/read"
    
    headersList = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "path": "/FileStore/Allen_mini_project11/alcohol_servings_by_type.png"
    })

    try:
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        response.raise_for_status()
        
        image_data = base64.b64decode(response.json()['data'])
        
        return send_file(
            BytesIO(image_data),
            mimetype='image/png',
            as_attachment=False
        )

    except requests.exceptions.RequestException as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response is not None:
            error_detail = e.response.text

        return jsonify({
            "error": "Request failed",
            "message": str(e),
            "details": error_detail
        }), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
