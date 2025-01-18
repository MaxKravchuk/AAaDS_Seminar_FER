import os
import shutil
import graphviz
import imageio.v2 as iio
from PIL import Image
import numpy as np
from avl_tree import AVLTree
from b_tree import BTreeNode

def _render_avl_to_png(avl_tree, filename, search_path=None):
    dot = graphviz.Digraph(comment="AVL Tree (PNG output)")
    dot.graph_attr["size"] = "10,6!"
    dot.graph_attr["dpi"] = "100"
    dot.engine = "dot"

    path_set = set(search_path) if search_path else set()

    def add_nodes_edges(node):
        if not node:
            return
        dot.node(str(id(node)), label=str(node.key))
        if node.left:
            if node in path_set and node.left in path_set:
                dot.edge(str(id(node)), str(id(node.left)), color="green", penwidth="3")
            else:
                dot.edge(str(id(node)), str(id(node.left)))
            add_nodes_edges(node.left)
        if node.right:
            if node in path_set and node.right in path_set:
                dot.edge(str(id(node)), str(id(node.right)), color="green", penwidth="3")
            else:
                dot.edge(str(id(node)), str(id(node.right)))
            add_nodes_edges(node.right)

    add_nodes_edges(avl_tree.root)
    dot.render(filename=filename, format="png", cleanup=True)

def create_avl_insertion_gif(avl_tree, values_to_insert, output_gif="avl_insertion.gif", fps=2):
    frames_dir = "temp_avl_insert_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    for i, val in enumerate(values_to_insert):
        avl_tree.insert_key(val)
        filename_no_ext = os.path.join(frames_dir, f"avl_insert_step_{i:04d}")
        _render_avl_to_png(avl_tree, filename_no_ext)

    png_files = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")
    ])
    with iio.get_writer(output_gif, mode='I', duration=1/fps) as writer:
        for png_path in png_files:
            img = Image.open(png_path)
            img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            frame = np.array(img_resized)
            writer.append_data(frame)

    shutil.rmtree(frames_dir)
    print(f"[AVL Insertion GIF] Created '{output_gif}', then deleted {frames_dir}.")

def create_avl_search_gif(avl_tree, values_to_search, output_gif="avl_search.gif", fps=2):
    frames_dir = "temp_avl_search_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    for i, val in enumerate(values_to_search):
        found, path = avl_tree.search_key_with_path(val)
        filename_no_ext = os.path.join(frames_dir, f"avl_search_step_{i:04d}")
        _render_avl_to_png(avl_tree, filename_no_ext, search_path=path)

    png_files = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")
    ])
    with iio.get_writer(output_gif, mode='I', duration=1/fps) as writer:
        for png_path in png_files:
            img = Image.open(png_path)
            img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            frame = np.array(img_resized)
            writer.append_data(frame)

    shutil.rmtree(frames_dir)
    print(f"[AVL Search GIF] Created '{output_gif}', then deleted {frames_dir}.")

def create_avl_deletion_gif(avl_tree, values_to_delete, output_gif="avl_deletion.gif", fps=2):
    frames_dir = "temp_avl_delete_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    for i, val in enumerate(values_to_delete):
        avl_tree.delete_key(val)
        filename_no_ext = os.path.join(frames_dir, f"avl_delete_step_{i:04d}")
        _render_avl_to_png(avl_tree, filename_no_ext)

    png_files = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")
    ])
    with iio.get_writer(output_gif, mode='I', duration=1/fps) as writer:
        for png_path in png_files:
            img = Image.open(png_path)
            img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            frame = np.array(img_resized)
            writer.append_data(frame)

    shutil.rmtree(frames_dir)
    print(f"[AVL Deletion GIF] Created '{output_gif}', then deleted {frames_dir}.")

def _render_btree_to_png(btree, filename, search_path=None):
    dot = graphviz.Digraph(comment="B-Tree (PNG output)")
    dot.graph_attr["size"] = "10,6!"
    dot.graph_attr["dpi"] = "100"
    dot.engine = "dot"

    path_set = set(search_path) if search_path else set()

    def btree_node_label(node: BTreeNode):
        keys_list = [str(node.keys[i]) for i in range(node.n)]
        return "|".join(keys_list)

    def add_nodes_edges(node, name_prefix="N"):
        if not node:
            return
        node_id = f"{name_prefix}{id(node)}"
        label_text = btree_node_label(node)
        dot.node(node_id, label="{" + label_text + "}", shape="record")
        if node.leaf:
            return
        for i in range(node.n + 1):
            child = node.children[i]
            if child is not None:
                child_id = f"{name_prefix}{id(child)}"
                if node in path_set and child in path_set:
                    dot.edge(node_id, child_id, color="green", penwidth="3")
                else:
                    dot.edge(node_id, child_id)
                add_nodes_edges(child, name_prefix)
    add_nodes_edges(btree.root)
    dot.render(filename=filename, format="png", cleanup=True)

def create_btree_insertion_gif(btree, values_to_insert, output_gif="btree_insertion.gif", fps=2):
    frames_dir = "temp_btree_insert_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    for i, val in enumerate(values_to_insert):
        btree.insert_key(val)
        filename_no_ext = os.path.join(frames_dir, f"btree_insert_step_{i:04d}")
        _render_btree_to_png(btree, filename_no_ext)

    png_files = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")
    ])
    with iio.get_writer(output_gif, mode='I', duration=1/fps) as writer:
        for png_path in png_files:
            img = Image.open(png_path)
            img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            frame = np.array(img_resized)
            writer.append_data(frame)

    shutil.rmtree(frames_dir)
    print(f"[B-Tree Insertion GIF] Created '{output_gif}', then deleted {frames_dir}.")

def create_btree_search_gif(btree, values_to_search, output_gif="btree_search.gif", fps=2):
    frames_dir = "temp_btree_search_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    for i, val in enumerate(values_to_search):
        found, path = btree.search_key_with_path(val)
        filename_no_ext = os.path.join(frames_dir, f"btree_search_step_{i:04d}")
        _render_btree_to_png(btree, filename_no_ext, search_path=path)

    png_files = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")
    ])
    with iio.get_writer(output_gif, mode='I', duration=1/fps) as writer:
        for png_path in png_files:
            img = Image.open(png_path)
            img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            frame = np.array(img_resized)
            writer.append_data(frame)

    shutil.rmtree(frames_dir)
    print(f"[B-Tree Search GIF] Created '{output_gif}', then deleted {frames_dir}.")

def create_btree_deletion_gif(btree, values_to_delete, output_gif="btree_deletion.gif", fps=2):
    frames_dir = "temp_btree_delete_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    for i, val in enumerate(values_to_delete):
        btree.delete_key(val)
        filename_no_ext = os.path.join(frames_dir, f"btree_delete_step_{i:04d}")
        _render_btree_to_png(btree, filename_no_ext)

    png_files = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")
    ])
    with iio.get_writer(output_gif, mode='I', duration=1/fps) as writer:
        for png_path in png_files:
            img = Image.open(png_path)
            img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            frame = np.array(img_resized)
            writer.append_data(frame)

    shutil.rmtree(frames_dir)
    print(f"[B-Tree Deletion GIF] Created '{output_gif}', then deleted {frames_dir}.")

def main():

    if not os.path.exists("./visuals"):
        os.makedirs("./visuals")

    data = [10, 5, 15, 2, 7, 12, 20]

    avl = AVLTree()
    create_avl_insertion_gif(avl, data, "./visuals/savl_insertion.gif", fps=1)
    create_avl_search_gif(avl, [7, 20, 99], "./visuals/avl_search.gif", fps=1)
    create_avl_deletion_gif(avl, [15, 5], "./visuals/avl_deletion.gif", fps=1)

    from b_tree import BTree
    b = BTree(t=2)
    create_btree_insertion_gif(b, data, "./visuals/btree_insertion.gif", fps=1)
    create_btree_search_gif(b, [6, 7, 99], "./visuals/btree_search.gif", fps=1)
    create_btree_deletion_gif(b, [6, 20], "./visuals/btree_deletion.gif", fps=1)

if __name__ == "__main__":
    main()