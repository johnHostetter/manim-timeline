import cv2  # pip install opencv-python
import torch
import gymnasium as gym
import matplotlib.pyplot as plt

from manim import *
from d3rlpy.datasets import get_cartpole


def get_data_and_env(n_samples=100):
    data, _ = get_cartpole(dataset_type="replay")
    X = torch.tensor(np.vstack(([episode.observations for episode in data.episodes])))
    X = X[np.lexsort((X[:, 0], X[:, 2]), axis=0)]
    idx = np.round(np.linspace(0, len(X) - 1, 100)).astype(int)
    X = X[idx]
    np.random.shuffle(X)
    env = gym.make("CartPole-v1", render_mode="rgb_array")
    env = env.unwrapped
    env.reset()
    return X[:n_samples], env


def display_cart_pole(env, state, scale, add_border=True):
    env.state = state
    img = plt.imshow(env.render())
    plt.grid(False)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("media/images/cartpole.png", dpi=100)

    if add_border:  # add a black border to the image
        img = cv2.imread("media/images/cartpole.png")
        img = cv2.copyMakeBorder(
            src=img,
            top=5,
            bottom=5,
            left=5,
            right=5,
            borderType=cv2.BORDER_CONSTANT,
        )
        cv2.imwrite("media/images/cartpole.png", img)

    return ImageMobject("media/images/cartpole.png")
