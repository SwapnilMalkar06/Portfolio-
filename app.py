from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your frontend to talk to this backend

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       # Default XAMPP user
app.config['MYSQL_PASSWORD'] = '852456'       # Default XAMPP password is empty
app.config['MYSQL_DB'] = 'portfolio_db'

mysql = MySQL(app)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()

        return jsonify({"status": "success", "message": "Feedback received!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)