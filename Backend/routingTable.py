from flask import Flask, request, jsonify
from signup import signup
from login import login
import dotenv
from accountTypeMannager import fetchUsers, updateAccountType

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World, from Flask!"

@app.route('/signup', methods=['POST'])
def runSignup():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON input"}), 400
    username = str(data['username'])
    password = str(data['password'])
    email = str(data['email'])
    try:
        if signup(username,password,email) == "user successfully created":
            return 'signup successful'
        else:
            return 'signup failed'
    except:
        return 'signup failed'
    

@app.route('/login', methods=['POST'])
def runLogin():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON input"}), 400
    email = data['email']
    password = data['password']
    try:
        if login(email,password) >= 0: 
            return 'login successful'
        elif login(email,password) == "invalid email or password":
                return 'invalid email or password'
        else:
            return 'login failed'
    except:
        return 'login failed'
    
@app.route('/AccountTypeMannager', methods=['GET', 'POST'])
def runAccountTypeMannager():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON input"}), 400
    targetUID = data['targetUID']
    newAccountType = data['newAccountType']
    UID = int(dotenv.get_key("UID"))
    try:
        print(fetchUsers(UID))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    try:
        if updateAccountType(UID, targetUID, newAccountType) == "User " + str(UID) + " updated account type for user " + str(targetUID):
            return 'account type updated successfully'
        elif updateAccountType(UID, targetUID, newAccountType) == "User not verified for this action":
            return 'user not verified for this action'
        else:
            return 'account type update failed'
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fetchUsers', methods=['POST','GET'])
def runFetchUsers():
    UID = int(dotenv.get_key("UID"))
    try:
        users = fetchUsers(UID)
        if isinstance(users, list):
            return jsonify(users), 200
        else:
            return jsonify({"error": users}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(debug=True)