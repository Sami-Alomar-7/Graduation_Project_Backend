from IPython.display import Image, display

def visualize_graph(graph):
        mermaid_png = graph.get_graph().draw_mermaid_png()
        display(Image(mermaid_png))
        with open('resources/images/graph.png', 'wb') as f:
            f.write(mermaid_png)
        print("(🎨) Graph saved to graph.png")