from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# Actions: 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
ACTIONS = {
    0: (-1, 0),  # UP
    1: (1, 0),   # DOWN
    2: (0, -1),  # LEFT
    3: (0, 1)    # RIGHT
}

def is_valid(r, c, n):
    return 0 <= r < n and 0 <= c < n

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    n = data.get('n')
    start = data.get('start')  # {r, c}
    end = data.get('end')      # {r, c}
    obstacles = data.get('obstacles') # list of {r, c}
    
    # Convert obstacles to tuples for easy checking
    obs_set = {(o['r'], o['c']) for o in obstacles}
    end_state = (end['r'], end['c'])

    # Generate random policy
    # For every cell, assign a random action
    policy_matrix = np.random.randint(0, 4, size=(n, n))
    
    # Policy Evaluation
    V = np.zeros((n, n))
    gamma = 0.9

    # Iterate until convergence with tolerance 1e-3
    # Cap at 1000 iterations to prevent infinite loops
    for _ in range(1000):
        delta = 0
        new_V = np.copy(V)
        for r in range(n):
            for c in range(n):
                # Terminal state or obstacles don't have active values
                if (r, c) == end_state or (r, c) in obs_set:
                    continue
                
                a = policy_matrix[r, c]
                dr, dc = ACTIONS[a]
                nr, nc = r + dr, c + dc
                
                # Default reward and value if hitting wall or obstacle
                if not is_valid(nr, nc, n) or (nr, nc) in obs_set:
                    next_v = V[r, c] # bounce back
                    reward = -1      # penalty for hitting 
                else:
                    next_v = V[nr, nc]
                    if (nr, nc) == end_state:
                        reward = 10  # Reach goal!
                    else:
                        reward = -1  # normal move
                
                # Deterministic transition
                new_val = reward + gamma * next_v
                new_V[r, c] = new_val
                delta = max(delta, abs(new_val - V[r, c]))
                
        V = new_V
        if delta < 1e-3:
            break

    # Format output
    # V matrix to list of lists, rounded
    v_list = np.round(V, 2).tolist()
    # Policy to arrows: 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
    arrow_map = {0: '↑', 1: '↓', 2: '←', 3: '→'}
    p_list = []
    for r in range(n):
        row = []
        for c in range(n):
            if (r, c) == end_state:
                row.append('G')
            elif (r, c) in obs_set:
                row.append('X')
            else:
                row.append(arrow_map[policy_matrix[r, c]])
        p_list.append(row)

    return jsonify({
        'value_matrix': v_list,
        'policy_matrix': p_list
    })

@app.route('/optimal_policy', methods=['POST'])
def optimal_policy():
    data = request.json
    n = data.get('n')
    end = data.get('end')
    obstacles = data.get('obstacles')
    
    obs_set = {(o['r'], o['c']) for o in obstacles}
    end_state = (end['r'], end['c'])

    # Value Iteration
    V = np.zeros((n, n))
    gamma = 0.9

    for _ in range(1000):
        delta = 0
        new_V = np.copy(V)
        for r in range(n):
            for c in range(n):
                if (r, c) == end_state or (r, c) in obs_set:
                    continue
                
                # Find max value over all actions
                max_val = float('-inf')
                for a in ACTIONS:
                    dr, dc = ACTIONS[a]
                    nr, nc = r + dr, c + dc
                    
                    if not is_valid(nr, nc, n) or (nr, nc) in obs_set:
                        next_v = V[r, c]
                        reward = -1
                    else:
                        next_v = V[nr, nc]
                        if (nr, nc) == end_state:
                            reward = 10
                        else:
                            reward = -1
                    
                    val = reward + gamma * next_v
                    if val > max_val:
                        max_val = val
                        
                new_V[r, c] = max_val
                delta = max(delta, abs(max_val - V[r, c]))
                
        V = new_V
        if delta < 1e-3:
            break

    # Extract Optimal Policy
    best_policy = np.zeros((n, n), dtype=int)
    for r in range(n):
        for c in range(n):
            if (r, c) == end_state or (r, c) in obs_set:
                continue
                
            best_a = 0
            max_val = float('-inf')
            # Argmax over actions
            for a in ACTIONS:
                dr, dc = ACTIONS[a]
                nr, nc = r + dr, c + dc
                
                if not is_valid(nr, nc, n) or (nr, nc) in obs_set:
                    next_v = V[r, c]
                    reward = -1
                else:
                    next_v = V[nr, nc]
                    if (nr, nc) == end_state:
                        reward = 10
                    else:
                        reward = -1
                
                val = reward + gamma * next_v
                # Break ties arbitrarily, strictly greater for simplicity
                if val > max_val:
                    max_val = val
                    best_a = a
            
            best_policy[r, c] = best_a

    # Format output
    v_list = np.round(V, 2).tolist()
    arrow_map = {0: '↑', 1: '↓', 2: '←', 3: '→'}
    p_list = []
    for r in range(n):
        row = []
        for c in range(n):
            if (r, c) == end_state:
                row.append('G')
            elif (r, c) in obs_set:
                row.append('X')
            else:
                row.append(arrow_map[best_policy[r, c]])
        p_list.append(row)

    return jsonify({
        'value_matrix': v_list,
        'policy_matrix': p_list
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)