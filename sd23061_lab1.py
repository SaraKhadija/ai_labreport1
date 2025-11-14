import streamlit as st
from collections import deque

# --- 1. Graph Definition ---
# The provided directed graph structure
GRAPH = {
    'A': ['D', 'B'],
    'B': ['C', 'E', 'G'],
    'C': ['A'],
    'D': ['C', 'A'],
    'E': ['H'],
    'F': [],
    'G': ['F'],
    'H': ['G', 'F']
}

# --- 2. Search Algorithm Implementations ---

def breadth_first_search(graph, start_node, goal_node):
    """
    Performs BFS with alphabetical tie-breaking.
    Returns (path, process_steps).
    """
    queue = deque([start_node])
    visited = {start_node}
    parent_map = {start_node: None}
    process_steps = []
    level = {start_node: 0}
    
    # Track the order nodes are expanded (moved from queue/stack to process_steps)
    expansion_order = 0
    
    # Initial setup for the table
    process_steps.append({
        'Step': expansion_order,
        'Expansion': 'Start',
        'Level': 0,
        'Frontier (Queue)': [start_node],
        'Visited': {start_node}
    })
    
    while queue:
        current_node = queue.popleft()
        expansion_order += 1
        
        # Check for goal immediately after expansion
        if current_node == goal_node:
            break
            
        # Get neighbors and apply alphabetical tie-breaking
        neighbors = sorted(graph.get(current_node, []))
        
        # New nodes added to the queue in alphabetical order
        new_frontier = list(queue)
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current_node
                level[neighbor] = level[current_node] + 1
                queue.append(neighbor)
                
        # Record the process step after expanding and adding new nodes
        process_steps.append({
            'Step': expansion_order,
            'Expansion': current_node,
            'Level': level[current_node],
            'Frontier (Queue)': new_frontier + sorted(list(queue)), # Show current queue state
            'Visited': visited.copy()
        })
    
    # Reconstruct Path
    path = []
    if current_node == goal_node:
        curr = goal_node
        while curr is not None:
            path.append(curr)
            curr = parent_map.get(curr)
        path.reverse()

    return path, process_steps, level

def depth_first_search(graph, start_node, goal_node):
    """
    Performs DFS with alphabetical tie-breaking.
    Returns (path, process_steps).
    """
    # DFS uses a stack (LIFO). Python lists can be used as a stack.
    stack = [start_node]
    visited = {start_node}
    parent_map = {start_node: None}
    process_steps = []
    level = {start_node: 0} # Level tracking is less standard in DFS but helpful for comparison
    
    expansion_order = 0
    
    # Initial setup for the table
    process_steps.append({
        'Step': expansion_order,
        'Expansion': 'Start',
        'Level': 0,
        'Frontier (Stack)': [start_node],
        'Visited': {start_node}
    })
    
    while stack:
        current_node = stack.pop()
        expansion_order += 1
        
        # Check for goal immediately after expansion
        if current_node == goal_node:
            break
            
        # Get neighbors. To ensure alphabetical tie-breaking works on a LIFO stack,
        # we must process them in REVERSE alphabetical order, so the alphabetically
        # first neighbor is pushed LAST and popped FIRST.
        neighbors = sorted(graph.get(current_node, []), reverse=True)
        
        # New nodes added to the stack
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current_node
                # Increment level from parent
                level[neighbor] = level[current_node] + 1 
                stack.append(neighbor)
        
        # Record the process step after expanding and adding new nodes
        process_steps.append({
            'Step': expansion_order,
            'Expansion': current_node,
            'Level': level[current_node],
            # Show current stack state (top of stack is the rightmost element)
            'Frontier (Stack)': stack[::-1], 
            'Visited': visited.copy()
        })
        
    # Reconstruct Path
    path = []
    if current_node == goal_node:
        curr = goal_node
        while curr is not None:
            path.append(curr)
            curr = parent_map.get(curr)
        path.reverse()
        
    return path, process_steps, level


# --- 3. Streamlit UI and Execution ---

def main():
    st.set_page_config(layout="wide")
    st.title("🗺️ Directed Graph Search Comparison (BFS vs. DFS)")
    
    st.image("LabReport_BSD2513_#1.jpg", caption="The Directed Graph")
    
    # Sidebar for User Input
    st.sidebar.header("Search Settings")
    nodes = sorted(list(GRAPH.keys()))
    start_node = st.sidebar.selectbox("Select Start Node:", nodes, index=nodes.index('A'))
    goal_node = st.sidebar.selectbox("Select Goal Node:", nodes, index=nodes.index('F'))
    
    st.sidebar.info("Tie-breaking Rule: **Alphabetical** (e.g., A before B, C before D)")
    
    # Check if a search should be run
    if st.sidebar.button("Run Search Algorithms"):
        
        # --- Run BFS ---
        st.header("1. Breadth-First Search (BFS)")
        st.subheader(f"Start: **{start_node}** | Goal: **{goal_node}** | Strategy: **FIFO Queue**")
        
        path_bfs, steps_bfs, level_bfs = breadth_first_search(GRAPH, start_node, goal_node)
        
        # Path and Level Discussion
        if path_bfs:
            st.success(f"Path Found: **{' -> '.join(path_bfs)}**")
            st.markdown(f"**Goal Node ({goal_node}) Level:** **{level_bfs[goal_node]}**")
        else:
            st.error("Path not found using BFS.")
            
        st.markdown("### Process Path & Frontier Discussion (Queue)")
        st.dataframe(
            pd.DataFrame(steps_bfs).style.set_properties(**{'text-align': 'left'}), 
            hide_index=True,
            column_config={
                'Frontier (Queue)': st.column_config.ListColumn("Frontier (Queue)"),
                'Visited': st.column_config.ListColumn("Visited")
            }
        )

        st.markdown("---")
        
        # --- Run DFS ---
        st.header("2. Depth-First Search (DFS)")
        st.subheader(f"Start: **{start_node}** | Goal: **{goal_node}** | Strategy: **LIFO Stack**")

        path_dfs, steps_dfs, level_dfs = depth_first_search(GRAPH, start_node, goal_node)
        
        # Path and Level Discussion
        if path_dfs:
            st.success(f"Path Found: **{' -> '.join(path_dfs)}**")
            st.markdown(f"**Goal Node ({goal_node}) Level:** **{level_dfs[goal_node]}**")
        else:
            st.error("Path not found using DFS.")

        st.markdown("### Process Path & Frontier Discussion (Stack)")
        st.dataframe(
            pd.DataFrame(steps_dfs).style.set_properties(**{'text-align': 'left'}), 
            hide_index=True,
            column_config={
                'Frontier (Stack)': st.column_config.ListColumn("Frontier (Stack)"),
                'Visited': st.column_config.ListColumn("Visited")
            }
        )
        
        st.markdown("---")
        st.header("🔍 Summary of Levels")
        col1, col2 = st.columns(2)
        
        col1.markdown("**BFS Levels (Shortest Path Level)**")
        col1.json({k: v for k, v in sorted(level_bfs.items())})

        col2.markdown("**DFS Levels (Path Depth)**")
        col2.json({k: v for k, v in sorted(level_dfs.items())})
        
        st.markdown("""
        **Note on Level:**
        * **BFS** finds the shortest path in terms of number of edges, so its reported level for a node is its **true minimum distance** from the start.
        * **DFS** explores depth-first; its reported level for a node is simply the **depth in the specific search tree** it followed, which is not necessarily the shortest distance.
        """)

if __name__ == "__main__":
    import pandas as pd
    main()