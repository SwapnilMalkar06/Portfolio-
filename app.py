from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '852456'  # Default XAMPP password is empty
app.config['MYSQL_DB'] = 'portfolio_db'

mysql = MySQL(app)

# Home route to serve the portfolio
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    cur = None
    try:
        # Check if connection is active
        if not mysql.connection:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500
            
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        
        return jsonify({"status": "success", "message": "Feedback received!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if cur:
            cur.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)