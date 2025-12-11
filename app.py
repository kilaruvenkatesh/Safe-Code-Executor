from flask_cors import CORS
from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)
CORS(app)    # Allow frontend to call API

@app.route("/run", methods=["POST"])
def run_code():

     # Safely get JSON input (avoid crashing on bad requests)
    data = request.get_json(silent=True)

    # ✅ Handle missing or empty code safely
    if not data or "code" not in data or not data["code"].strip():
        return jsonify({
            "output": "No code provided. Please enter some Python code."
        })

    code = data["code"]

    # ✅ Code length protection (5000 characters)
    if len(code) > 5000:
        return jsonify({
            "output": "Code too long. Maximum allowed length is 5000 characters."
        })
 # Create unique temporary file
    filename = f"{uuid.uuid4()}.py"
 # Save code into the file
    with open(filename, "w") as f:
        f.write(code)

    try:
         # Execute inside Docker sandbox
        result = subprocess.run(
            [
                "docker", "run",
                "--rm",
                "--read-only",
                "--cpus=1",
                "--memory=128m",
                "--network", "none",
                "-v", f"{os.getcwd()}:/app",
                "python:3.11-slim",
                "python", f"/app/{filename}"
            ],
            capture_output=True,
            text=True,
            timeout=10   # Kill infinite loops
        )

        output = result.stdout + result.stderr

    except subprocess.TimeoutExpired:
        output = "Execution timed out after 10 seconds"

    except Exception as e:
        output = str(e)

    finally:
          # Remove temporary file
        if os.path.exists(filename):
            os.remove(filename)

    return jsonify({"output": output})


if __name__ == "__main__":
    app.run(debug=True)
