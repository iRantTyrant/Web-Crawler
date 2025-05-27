#Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_similarity(matrix, filename, labels=None, fontsize=10):

    # Check if the input is a DataFrame if not make it one
    if not isinstance(matrix, pd.DataFrame):
        df = pd.DataFrame(matrix)
        if labels:
            df.index = labels
            df.columns = labels

    else:
        df = matrix.copy()
        if labels:
            df.index = labels
            df.columns = labels

    fig, axs = plt.subplots(1, 2, figsize=(18, len(df) * 0.6))  #Two subplots side by side
    plt.subplots_adjust(wspace=0.5)

    # ---Matrix---
    axs[0].axis('off')
    table = axs[0].table(cellText=df.round(2).values,
                         rowLabels=df.index,
                         colLabels=df.columns,
                         cellLoc='center',
                         loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(1.2, 1.2)
    axs[0].set_title("Similarity Matrix Table", fontsize=fontsize+2)

    # --- Heatmap ---
    sns.heatmap(df, annot=False, cmap="YlGnBu", xticklabels=True, yticklabels=True, ax=axs[1])
    axs[1].set_title("Heatmap", fontsize=fontsize+2)

    #In case of large labels, rotate them for better visibility
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].tick_params(axis='y', rotation=0)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"[✔] Saved combined image to: {filename}")
