from flask import Flask, request, jsonify, send_from_directory
from flasgger import Swagger
import pandas as pd

app = Flask(__name__)
swagger = Swagger(app)

users = []

@app.route('/users/<name>/<int:age>', methods=['POST'])
def create_user(name, age):
    """
    Create a new user
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: User's name to add
      - name: age
        in: path
        type: integer
        required: true
        description: User's age to add
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid input
    """
    if not isinstance(age, int) or age < 0 or age > 120:
        return jsonify({'message': 'Invalid input: age must be an integer between 0 and 120'}), 400
    users.append({'name': name, 'age': age})
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    """
    Delete a user by name
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: User's name to delete
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    global users
    user_exists = any(user['name'] == name for user in users)
    if user_exists:
        users = [user for user in users if user['name'] != name]
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get a list of all users
    ---
    responses:
      200:
        description: A list of users
    """
    return jsonify(users), 200

@app.route('/users/csv', methods=['POST'])
def add_users_from_csv():
    """
    Add multiple users from a CSV file
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The CSV file containing user data
    responses:
      201:
        description: Users added successfully
      400:
        description: Invalid file or data
    """
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()
            for _, row in df.iterrows():
                name = row['name']
                age = row['age']
                users.append({'name': name, 'age': age})
            return jsonify({'message': 'Users added successfully'}), 201
        except Exception as e:
            return jsonify({'message': f'Invalid data: {str(e)}'}), 400

@app.route('/users/average_age', methods=['GET'])
def get_average_age():
    """
    Calculate the average age of users, grouped by the first character of their usernames
    ---
    responses:
      200:
        description: A dictionary containing the average age for each group
    """
    df = pd.DataFrame(users)
    if df.empty:
        return jsonify({}), 200
    df['group'] = df['name'].str[0]
    average_ages = df.groupby('group')['age'].mean().to_dict()
    return jsonify(average_ages), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')