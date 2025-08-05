from dotenv import load_dotenv
from src.graphs.graph_builders import compiled_graph
from src.schemas.states import initial_state
from src.configs import config
from src.graphs.graph_visualizers import visualize_graph
from src.databases.database import character_db
load_dotenv()

if __name__ == "__main__":
    visualize_graph(compiled_graph)
    character_db.clear_database()
    response = compiled_graph.invoke(initial_state, config=config)
    print(response)