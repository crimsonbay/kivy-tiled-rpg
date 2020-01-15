import os
import pickle


def save_col_file(collisions, collisions_count, tilesize, collision_filename):
    obj = {'collisions': dict(collisions), 'collisions_count': collisions_count, 'tilesize': list(tilesize)}
    with open(collision_filename, 'wb') as f:
        pickle.dump(obj, f)


def load_col_file(collision_filename):
    if (not os.path.isfile(collision_filename)) or (not os.path.exists(collision_filename)):
        return None
    with open(collision_filename, 'rb') as f:
        return pickle.load(f)
