import logging
import threading
import time
import psutil
from config.settings import HEARTBEAT_INTERVAL, HEARTBEAT_ENABLED

logger = logging.getLogger("tracker")

SAFE_MIN_INTERVAL = 10   # seconds
SAFE_MAX_INTERVAL = 600  # seconds

class Tracker:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.heartbeat_thread = None
        self.running = False

        # Validate heartbeat interval
        if HEARTBEAT_ENABLED:
            if HEARTBEAT_INTERVAL < SAFE_MIN_INTERVAL:
                logger.warning(
                    f"⚠️ Heartbeat interval too low ({HEARTBEAT_INTERVAL}s). "
                    f"Clamping to {SAFE_MIN_INTERVAL}s to avoid excessive CPU/logging costs."
                )
                self.interval = SAFE_MIN_INTERVAL
            elif HEARTBEAT_INTERVAL > SAFE_MAX_INTERVAL:
                logger.warning(
                    f"⚠️ Heartbeat interval too high ({HEARTBEAT_INTERVAL}s). "
                    f"Clamping to {SAFE_MAX_INTERVAL}s. Lower intervals reduce risk of runaway logs."
                )
                self.interval = SAFE_MAX_INTERVAL
            else:
                self.interval = HEARTBEAT_INTERVAL
        else:
            self.interval = None

    def log_request(self):
        self.request_count += 1

    def get_stats(self):
        uptime = time.time() - self.start_time
        cpu_usage = psutil.cpu_percent(interval=0.5)
        mem_usage = psutil.virtual_memory().percent
        return {
            "uptime_sec": round(uptime, 2),
            "requests": self.request_count,
            "cpu_percent": cpu_usage,
            "mem_percent": mem_usage
        }

    def log_stats(self):
        stats = self.get_stats()
        logger.info(f"📊 Stats: {stats}")
        return stats

    def start_heartbeat(self):
        if not HEARTBEAT_ENABLED:
            return
        if self.running:
            return
        self.running = True

        def heartbeat_loop():
            while self.running:
                self.log_stats()
                time.sleep(self.interval)

        self.heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def stop_heartbeat(self):
        self.running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join()

# Singleton tracker
tracker = Tracker()
