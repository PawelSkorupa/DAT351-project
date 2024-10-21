from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Add ProxyFix to handle headers properly in Lambda
app.wsgi_app = ProxyFix(app.wsgi_app)

tasks = []

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = {"id": len(tasks) + 1, "task": data['task']}
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = next((task for task in tasks if task["id"] == id), None)
    if task:
        tasks.remove(task)
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
