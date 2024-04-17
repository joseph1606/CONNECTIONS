import matplotlib.pyplot as plt

def visualize_author_node(author_node):
    # Create a plot
    plt.figure(figsize=(10, 6))

    # Plot the author node
    plt.text(
        0.5,
        0.5,
        f"Author: {author_node.name}\nAliases: {', '.join(author_node.aliases)}\nURL: {author_node.url}",
        ha="center",
        va="center",
        bbox=dict(facecolor="lightblue", alpha=0.5),
    )

    # Plot the papers
    for i, paper in enumerate(author_node.papers):
        plt.text(
            0.5,
            0.3 - 0.15 * i,
            f"Paper {i+1}:\nTitle: {paper.title}\nYear: {paper.year}\nAuthors: {', '.join(paper.authors)}",
            ha="center",
            va="center",
            bbox=dict(facecolor="lightgreen", alpha=0.5),
        )

    plt.axis("off")
    plt.title("Author and Papers")
    plt.show()
