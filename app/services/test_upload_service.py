from flask import  request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import csv
import json


class UploadService :


    def handle_upload(self, file):
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        
        processing_result = {}
        message = ""
        
        try:
            # Process the file content based on its extension
            file_content = file.stream.read().decode("utf-8")

            if extension == 'csv':
                csv_reader = csv.reader(file_content.splitlines())
                headers = next(csv_reader)
                first_row = next(csv_reader, None) # Safely get the first row
                processing_result = {"filename": filename, "headers": headers, "first_data_row": first_row}
                message = "CSV file processed successfully!"

            elif extension == 'json':
                data = json.loads(file_content)
                summary = {}
                if isinstance(data, list):
                    summary['type'] = 'list'
                    summary['item_count'] = len(data)
                    if data and isinstance(data[0], dict):
                        summary['first_item_keys'] = list(data[0].keys())
                elif isinstance(data, dict):
                    summary['type'] = 'dictionary'
                    summary['keys'] = list(data.keys())
                
                processing_result = {"filename": filename, "summary": summary}
                message = "JSON file processed successfully!"

        except Exception as e:
            return jsonify({"error": f"Failed to process file: {str(e)}"}), 500
        
        #  Process the optional JSON metadata from the form data
        metadata = {}
        if 'metadata' in request.form:
            try:
                metadata = json.loads(request.form['metadata'])
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid JSON in metadata field"}), 400

        return jsonify({"message": message, "file_summary": processing_result, "metadata": metadata}), 200


    pass 