import csv
from flask import g

class RedisKeyCreator:

    def createKeyByCSVReader(self, filename:str, csv_reader):
        headers = next(csv_reader)
        processing_result = {}
        message = ""
        rows_added = 0

        # Use a pipeline to efficiently add all rows to Redis
        with g.redis_client.pipeline() as pipe:
            for i, row in enumerate(csv_reader):                        
                # Create a unique key for each row, e.g., "csv:data.csv:0"
                redis_key = f"csv:{filename}:{i}"
                # Map headers to row values
                row_data = dict(zip(headers, row))
                # Add the HSET command to the pipeline
                pipe.hset(redis_key, mapping=row_data)
            
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

    pass