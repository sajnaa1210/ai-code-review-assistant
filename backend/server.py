import os

from flask import Flask, jsonify, request

from review_engine import ReviewEngineError, review_code

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/review", methods=["POST"])
def review():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json()
    code = payload.get("code")
    use_mock = bool(payload.get("use_mock", False))

    if not isinstance(code, str) or not code.strip():
        return jsonify({"error": "Missing non-empty 'code' field."}), 400

    try:
        result = review_code(code, use_mock=use_mock)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except ReviewEngineError as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
