from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "'title' must be a non-empty string"}), 400

    new_id = max((e.id for e in events), default=0) + 1
    event = Event(new_id, title.strip())
    events.append(event)
    return jsonify(event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "'title' must be a non-empty string"}), 400

    for e in events:
        if e.id == event_id:
            e.title = title.strip()
            return jsonify(e.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for i, e in enumerate(events):
        if e.id == event_id:
            deleted = events.pop(i)
            return jsonify({"message": "Event deleted", "event": deleted.to_dict()}), 200

    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
