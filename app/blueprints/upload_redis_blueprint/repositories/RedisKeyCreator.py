import csv
from flask import g,session,jsonify
import json
from redis.commands.json.path import Path


class RedisKeyCreator:

    def createKeyByCSVReader(self, filename:str, csv_reader):
        headers = next(csv_reader)
        processing_result = {}
        message = ""
        rows_added = 0
        session_id = session.sid

        # Use a pipeline to efficiently add all rows to Redis
        with g.redis_client.pipeline() as pipe:
            for i, row in enumerate(csv_reader):                        
                # Create a unique key for each row, e.g., "csv:data.csv:0"
                redis_key = f"csv:{session_id}:{i}"
                # Map headers to row values
                row_data = dict(zip(headers, row))
                # Add the HSET command to the pipeline
                pipe.hset(redis_key, mapping=row_data)
                pipe.expire(redis_key, 3600*3) # Three hours (time of live)
                rows_added += 1
            
            # Execute all commands in the pipeline at once if rows were found
            if rows_added > 0:
                pipe.execute()
            processing_result = {
                    "filename": filename,
                    "headers": headers,
                    "rows_added_to_redis": rows_added
                }
            message = f"CSV file processed successfully! Added {rows_added} rows to Redis."
        return processing_result, message, rows_added

        pass

    def createKeyByJSONReader(self, filename:str, data):
        processing_result = {}
        message = ""
        session_id = session.sid
        redis_client = g.redis_client
        errors = []
        summary = {}
        added_count = 0
        failed_count = 0

        # Handle JSON object input
        if isinstance(data, dict):
            summary['type'] = 'dictionary'
            summary['keys'] = list(data.keys())
            print("Processing JSON dictionary input.")
            
        # Handle JSON array input by treating indices as keys
        elif isinstance(data, list):
            summary['type'] = 'list'
            summary['item_count'] = len(data)
            print("Processing JSON array input (using index as key).")
        else:
            return jsonify({"status": "error", "message": "JSON data must be an object (dictionary) or an array"}), 400

        redisKey = ""
        try:
            redisKey = f"json:{session_id}"
            # Convert value to JSON string if it's a instance of list/dict.
            if isinstance(data, (dict, list)):
                redis_client.json().set(redisKey, Path.root_path(), data)
                # redis_client.set(redisKey, json.dumps(value))
                redis_client.expire(redisKey, 3600*3) # Three hours (time of live)
            else:
                # Otherwise, it will be stored as its string representation.
                redis_client.set(redisKey, str(data)) # Store as string
            added_count += 1
        except Exception as e:
            failed_count += 1
            errors.append(f"Failed to add key '{redisKey}': {e}")
            print(f"Error adding key '{redisKey}' to Redis: {e}")


        processing_result = {"filename": filename, "summary": summary}
        message = "JSON file processed successfully!"
        return processing_result, message

    pass