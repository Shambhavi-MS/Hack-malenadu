# ═══════════════════════════════════════════════════════════════
# launch.py — ThreatForge Master Launcher
# Run this file to start the desktop agent: python launch.py
# ═══════════════════════════════════════════════════════════════

from desktop_app import ThreatForgeApp

def main():
    print("🚀 Starting ThreatForge Desktop Agent...")
    app = ThreatForgeApp()
    print("✅ ThreatForge is running!")
    print("   → Click START AGENT in the window to begin monitoring")
    app.mainloop()

if __name__ == "__main__":
    main()
