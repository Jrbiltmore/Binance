import time
import logging
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlgorithmicThrottling:
    def __init__(self, rate_limit, time_window):
        """
        Initialize the AlgorithmicThrottling with rate limit and time window.

        :param rate_limit: Maximum number of requests allowed in the time window
        :param time_window: Time window in seconds for the rate limit
        """
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_times = deque()
        logger.info(f"AlgorithmicThrottling initialized with rate limit: {rate_limit} requests per {time_window} seconds")

    def can_proceed(self):
        """
        Check if a new request can proceed under the rate limit.

        :return: Boolean indicating whether the request can proceed
        """
        current_time = time.time()
        while self.request_times and self.request_times[0] <= current_time - self.time_window:
            self.request_times.popleft()
        if len(self.request_times) < self.rate_limit:
            return True
        return False

    def record_request(self):
        """
        Record a new request.

        :raises Exception: If the request cannot proceed due to rate limit
        """
        if not self.can_proceed():
            logger.warning("Rate limit exceeded. Request cannot proceed.")
            raise Exception("Rate limit exceeded. Please wait before making new requests.")
        self.request_times.append(time.time())
        logger.info("Request recorded successfully.")

    def wait_for_slot(self):
        """
        Wait until a slot is available for a new request.

        :return: None
        """
        while not self.can_proceed():
            time_to_wait = self.request_times[0] + self.time_window - time.time()
            if time_to_wait > 0:
                logger.info(f"Rate limit exceeded. Waiting for {time_to_wait:.2f} seconds.")
                time.sleep(time_to_wait)
        self.record_request()

# Example usage:
if __name__ == "__main__":
    rate_limit = 5  # Example rate limit of 5 requests
    time_window = 60  # Example time window of 60 seconds

    throttler = AlgorithmicThrottling(rate_limit, time_window)

    # Simulate making 6 requests
    for i in range(6):
        try:
            throttler.wait_for_slot()
            print(f"Request {i+1} processed")
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
