# ═══════════════════════════════════════════════════════════════
# agent.py — ThreatForge Background Monitoring Agent
# ═══════════════════════════════════════════════════════════════

import threading
import time
import random
from datetime import datetime
from plyer import notification

# ── Try to use real SHIELD, fall back to mock if not available ──
try:
    from shield import predict
    import joblib

    SHIELD_AVAILABLE = True

    # Load label encoder (IMPORTANT)
    try:
        le = joblib.load("le.pkl")   # make sure this file exists
    except:
        le = None
        print("⚠ Label encoder (le.pkl) not found — switching to mock mode")
        SHIELD_AVAILABLE = False

except ImportError:
    SHIELD_AVAILABLE = False
    print("⚠ shield.py not found — using fake predictions for now")


class ThreatAgent:

    def __init__(self, interval=3, on_event=None):
        self.interval = interval
        self.on_event = on_event
        self.running  = False
        self.thread   = None

        self.total_checked = 0
        self.attacks_found = 0
        self.safe_found    = 0
        self.log           = []

    def _generate_traffic(self):
        is_attack = random.random() < 0.35
        return {
            'duration':        random.randint(0,5) if is_attack else random.randint(5,60),
            'src_bytes':       random.randint(7000,10000) if is_attack else random.randint(100,2000),
            'dst_bytes':       random.randint(0,100) if is_attack else random.randint(100,2000),
            'num_connections': random.randint(300,500) if is_attack else random.randint(1,30),
            'error_rate':      random.uniform(0.7,1.0) if is_attack else random.uniform(0,0.1),
        }

    def _mock_predict(self, traffic):
        is_attack = traffic['src_bytes'] > 5000 or traffic['error_rate'] > 0.5
        return {
            'label':      '🚨 ATTACK DETECTED' if is_attack else '✅ SAFE',
            'confidence': f"{random.uniform(88,99):.1f}%",
            'timestamp':  datetime.now().strftime("%H:%M:%S"),
        }

    def _send_notification(self, result):
        try:
            notification.notify(
                title="🚨 ThreatForge — ATTACK DETECTED",
                message=f"{result['label']} | {result['confidence']}",
                app_name="ThreatForge",
                timeout=5,
            )
        except Exception as e:
            print(f"Notification error: {e}")

    def _run_loop(self):
        while self.running:
            traffic = self._generate_traffic()

            # ✅ FIXED PART
            if SHIELD_AVAILABLE and le is not None:
                try:
                    result = predict(le, traffic)
                except Exception as e:
                    print(f"Prediction error: {e}")
                    result = self._mock_predict(traffic)
            else:
                result = self._mock_predict(traffic)

            # Update counters
            self.total_checked += 1

            if 'ATTACK' in result['label']:
                self.attacks_found += 1
                self._send_notification(result)
            else:
                self.safe_found += 1

            # Log
            self.log.append(result)
            if len(self.log) > 100:
                self.log.pop(0)

            if self.on_event:
                self.on_event(result)

            time.sleep(self.interval)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("✅ ThreatForge Agent started")

    def stop(self):
        self.running = False
        print("🛑 ThreatForge Agent stopped")

    def get_stats(self):
        rate = (self.attacks_found / self.total_checked * 100) if self.total_checked > 0 else 0
        return {
            'total':   self.total_checked,
            'attacks': self.attacks_found,
            'safe':    self.safe_found,
            'rate':    f"{rate:.1f}%",
            'log':     self.log[-20:]
        }
