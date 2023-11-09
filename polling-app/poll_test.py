from flask import Flask,render_template
from flask_socketio import SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)


polls = [ 
    {"question": "Favorite Color", "options": {"Red": 0, "Blue": 0, "Green": 0}},
    {"question": "Best Programming Language", "options": {"Python": 0, "JavaScript": 0, "Java": 0}},    
]

@app.route('/')
def index():
    poll_data = []
    parent_index = 0
    for poll in polls:
        options_with_counts = [(option, count) for option, count in poll['options'].items()]
        poll_data.append({
            'question': poll['question'],
            'options': options_with_counts,
            'parent_index': parent_index
        })
        parent_index += 1
    return render_template('index_test.html',poll_data = poll_data)

@socketio.on('submit_vote')
def submit_vote(data):
    print(data)
    parent_idx = int(data['parent_idx'])
    poll_id = int(data['poll_id'])
    option = data['option']
    print(f"parent_idx: {parent_idx}, poll_id: {poll_id}, option: {option}")
    polls[parent_idx]["options"][option] += 1
    emit('update_results', {'parent_idx': parent_idx, 'poll_id': poll_id, 'option':option}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True) 
