from .game_2048 import Game2048
import gym


class Env2048(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = None

    def step(self, action):
        assert action in Game2048.valid_inputs

        reward = self.game.swipe(action)
        state = self.game.state
        done = not self.game.running
        info = {}

        return state, reward, done, info

    def reset(self):
        self.game = Game2048()
        return self.game.state

    def render(self, mode='human'):
        if mode == 'human':
            print(self.game)


if __name__ == '__main__':
    env = Env2048()
    state = env.reset()
    print(state)
    done = False
    while not done:
        action = input('action: ')
        state, reward, done, info = env.step(action)
        print(reward, done, info)
        print(state)
