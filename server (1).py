"""
RX Gesture Control - Server
============================
Hii ni server ndogo inayoendeshwa na Termux. Inapokea amri kutoka
kwenye browser (HTML + MediaPipe) na kuziendesha kama amri za Android
kwa kutumia termux-api.

Jinsi ya kuendesha:
    python server.py

Kisha fungua browser (kwenye simu hiyo hiyo) na nenda:
    http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify, send_from_directory
import subprocess
import time

app = Flask(__name__)

# Tunaweka muda wa mwisho gesture ilipotambuliwa, ili tusirudie
# amri mara nyingi mno kwa sekunde moja (debounce)
last_action_time = 0
COOLDOWN_SECONDS = 1.0  # subiri sekunde 1 kati ya amri mbili


def get_current_volume():
    """Soma volume ya sasa ya media kutoka kwa termux-volume."""
    try:
        result = subprocess.run(
            ["termux-volume"], capture_output=True, text=True, timeout=5
        )
        # termux-volume hutoa JSON yenye taarifa za stream tofauti (music, ring, n.k.)
        import json
        data = json.loads(result.stdout)
        for stream in data:
            if stream.get("stream") == "music":
                return stream.get("volume", 0), stream.get("max_volume", 15)
    except Exception as e:
        print("Imeshindikana kusoma volume:", e)
    return None, None


@app.route("/")
def home():
    """Tuma faili la index.html (interface ya kamera)."""
    return send_from_directory(".", "index.html")


@app.route("/gesture", methods=["POST"])
def handle_gesture():
    """
    Endpoint hii inapokea gesture kutoka kwenye JavaScript (browser).
    Tunatarajia JSON kama: {"gesture": "open_palm"} au {"gesture": "fist"}
    """
    global last_action_time

    data = request.get_json()
    gesture = data.get("gesture", "")

    now = time.time()
    if now - last_action_time < COOLDOWN_SECONDS:
        # Bado tunasubiri cooldown, puuza gesture hii
        return jsonify({"status": "ignored", "reason": "cooldown"})

    message = ""

    if gesture == "open_palm":
        # Mkono wazi -> ongeza volume
        volume, max_vol = get_current_volume()
        if volume is not None and volume < max_vol:
            subprocess.run(["termux-volume", "music", str(volume + 1)])
            message = f"Volume imeongezwa: {volume + 1}/{max_vol}"
        else:
            message = "Volume iko juu kabisa"
        last_action_time = now

    elif gesture == "fist":
        # Ngumi -> punguza volume
        volume, max_vol = get_current_volume()
        if volume is not None and volume > 0:
            subprocess.run(["termux-volume", "music", str(volume - 1)])
            message = f"Volume imepunguzwa: {volume - 1}/{max_vol}"
        else:
            message = "Volume iko chini kabisa"
        last_action_time = now

    else:
        message = f"Gesture haijulikani: {gesture}"

    print(message)
    return jsonify({"status": "ok", "message": message})


if __name__ == "__main__":
    print("=" * 50)
    print("RX Gesture Control - Server inaanza...")
    print("Fungua browser na nenda: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)
