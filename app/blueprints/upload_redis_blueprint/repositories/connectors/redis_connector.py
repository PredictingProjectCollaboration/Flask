from flask import current_app
import redis

class RConnector:
    """
    A connector class to manage and provide connections to a Redis instance.
    It follows a singleton-like pattern for the connection client within
    the application context to avoid creating multiple connections.
    """

    def __init__(self):
        """
        Initializes the connector using configuration from the Flask app context.
        It expects REDIS_HOST, REDIS_PORT, and REDIS_DB in the app config.
        """
        self.host = current_app.config.get('REDIS_HOST', 'localhost')
        self.port = current_app.config.get('REDIS_PORT', 6379)
        self.db = current_app.config.get('REDIS_DB', 0)
        self.client = None

    def get_connection(self):
        """
        Establishes and returns a connection to the Redis server.
        Caches the connection client to avoid reconnecting on every call.
        """
        if self.client is None:
            try:
                # decode_responses=True makes the client return Python strings instead of bytes.
                self.client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    decode_responses=True
                )
                # Test the connection immediately to fail fast if Redis is down.
                self.client.ping()
                current_app.logger.info(f"Successfully connected to Redis at {self.host}:{self.port}")
            except redis.exceptions.ConnectionError as e:
                current_app.logger.error(f"Failed to connect to Redis: {e}")
                # Re-raise the exception to let the caller know the connection failed.
                raise e
        return self.client

    def test_connection(self):
        """Tests the connection to Redis by sending a PING command."""
        try:
            conn = self.get_connection()
            return conn.ping()
        except redis.exceptions.ConnectionError:
            return False