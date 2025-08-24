from flask import Flask, jsonify
import requests

app = Flask(__name__)
BASE_URL = "https://api.github.com/users"

def fetch_user_data(username, depth, visited):
    if username in visited or depth == 0:
        return None
    visited.add(username)

    user_url = f"{BASE_URL}/{username}"
    user = requests.get(user_url).json()
    if "login" not in user:
        return None

    followers = requests.get(user_url + "/followers").json()
    following = requests.get(user_url + "/following").json()

    return {
        "login": user["login"],
        "avatar_url": user["avatar_url"],
        "followers": [f["login"] for f in followers],
        "following": [f["login"] for f in following],
        "children": [
            fetch_user_data(f["login"], depth-1, visited) for f in followers[:3]  # limit
        ] + [
            fetch_user_data(f["login"], depth-1, visited) for f in following[:3]
        ]
    }

@app.route("/network/<username>", methods=["GET"])
def get_network(username):
    visited = set()
    data = fetch_user_data(username, depth=2, visited=visited)  # depth=2 by default
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
