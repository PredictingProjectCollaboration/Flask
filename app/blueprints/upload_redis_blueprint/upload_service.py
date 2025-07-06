from flask import  request, jsonify, current_app, g
import redis
from werkzeug.utils import secure_filename
import os
import csv
import json
from werkzeug.datastructures import FileStorage
from .repositories.RedisKeyCreator import RedisKeyCreator


class UploadService :

    def __init__(self):
        self.redisKeyCreator = RedisKeyCreator()

        pass


    def handle_upload(self, file:FileStorage):
        g.redis_client.ping()
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        rows_added = 0
        processing_result = {}
        message = ""
        
        try:
            # Process the file content based on its extension
            file_content = file.stream.read().decode("utf-8")

            if extension == 'csv':
                csv_reader = csv.reader(file_content.splitlines())
                processing_result, message, rows_added = self.redisKeyCreator.createKeyByCSVReader(filename, csv_reader)

            elif extension == 'json':
                data = json.loads(file_content)            
                processing_result, message = self.redisKeyCreator.createKeyByJSONReader(filename, data)
    

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