from flask import Blueprint, request, jsonify, current_app
# from .upload_service import UploadService
# from . import upload_bp
from .upload_service import UploadService
from . import upload_bp

def allowed_file(filename):
    """Checks if the file's extension is allowed."""
    # This will check against the ALLOWED_EXTENSIONS set in your config
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', set())

@upload_bp.route('/upload', methods=['POST'])
def handle_upload():
    """
    Receives a multipart/form-data request containing a file and optional JSON metadata.
    Handles CSV and JSON file processing.
    """
    # 1. Check if the file part is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    # 2. Check if a file was actually selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 3. Check if the file is valid and has an allowed extension
    if file and allowed_file(file.filename):
        uploadService = UploadService()
        return uploadService.handle_upload(file)
    else:
        return jsonify({"error": "File type not allowed"}), 400
