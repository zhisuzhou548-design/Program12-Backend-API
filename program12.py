
import re
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def error_response(errors):
    return jsonify({
        "success": False,
        "status_code": 400,
        "message": "Validation Error",
        "errors": errors
    }), 400


@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Program 12 - AI Improved API</title>
        <style>
            body {
                font-family: Arial;
                background: #eef2f7;
                padding: 50px;
            }
            .container {
                background: white;
                padding: 30px;
                max-width: 500px;
                margin: auto;
                border-radius: 12px;
            }
            input, button {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                box-sizing: border-box;
            }
            button {
                background: #1769aa;
                color: white;
                border: none;
                cursor: pointer;
            }
            pre {
                background: #edf0f4;
                padding: 15px;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AI Improved Registration API</h2>
            <form id="registerForm">
                <input id="name" placeholder="Enter student name">
                <input id="email" placeholder="Enter email address">
                <button type="submit">Register</button>
            </form>
            <h3>API Response:</h3>
            <pre id="output">Waiting for input...</pre>
        </div>

        <script>
            document.getElementById('registerForm')
            .addEventListener('submit', async function(e) {
                e.preventDefault();

                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: document.getElementById('name').value,
                        email: document.getElementById('email').value
                    })
                });

                const result = await response.json();

                document.getElementById('output').textContent =
                    JSON.stringify(result, null, 4);
            });
        </script>
    </body>
    </html>
    """)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()

    errors = {}

    if not name:
        errors["name"] = "Name is required"

    if not email:
        errors["email"] = "Email is required"
    elif not is_valid_email(email):
        errors["email"] = "Invalid email format. Please provide a valid email address"

    if errors:
        return error_response(errors)

    return jsonify({
        "success": True,
        "status_code": 201,
        "message": f"User {name} registered successfully",
        "data": {
            "name": name,
            "email": email
        }
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
