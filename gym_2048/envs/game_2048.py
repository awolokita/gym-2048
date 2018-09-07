import numpy as np


class Game2048:
    UP = 'w'
    RIGHT = 'd'
    DOWN = 's'
    LEFT = 'a'
    valid_inputs = [UP, RIGHT, DOWN, LEFT]

    num2colour = {0: '37',
                  2: '93',
                  4: '33',
                  8: '91',
                  16: '31',
                  32: '95',
                  64: '35',
                  128: '94',
                  256: '34',
                  512: '96',
                  1024: '36',
                  2048: '97'}

    rot_dict = {UP: 0,
                RIGHT: 1,
                DOWN: 2,
                LEFT: 3}

    def __init__(self):
        # Set up the empty game board
        self.board = np.zeros([4, 4])

        # Randomly set two positions to 2
        rows = self.board.shape[0]
        cols = self.board.shape[1]

        a = []
        for i in range(rows):
            for j in range(cols):
                a.append((i, j))

        pos = np.random.choice(len(a), 2, replace=False)
        self.board[a[pos[0]]] = 2
        self.board[a[pos[1]]] = 2

        self.score = 0
        self.running = True

    def __repr__(self):
        rows = self.board.shape[0]
        cols = self.board.shape[1]
        s = '{0}\n===============\n'.format(self.score)
        for i in range(rows):
            for j in range(cols):
                n = int(self.board[i, j])
                c = '\033[' + Game2048.num2colour[n] + 'm'
                s += c + str(n) + '\033[0m'
                if j < (cols - 1):
                    s += '  '
            s += '\n'
        return s + '==============='

    @property
    def state(self):
        return np.copy(self.board)

    def _do_swipe(self, direction):
        if direction not in Game2048.valid_inputs:
            return
        swipe_score = 0
        changed = False

        # Take a working copy of the board
        board = np.copy(self.board)

        # Rotate the board by appropriate amount for direction of swipe
        board = np.rot90(board, Game2048.rot_dict[direction])

        num_cols = board.shape[1]
        for i in range(num_cols):
            a = np.copy(board[:, i])

            idx = np.nonzero(a)[0]
            if len(idx) > 0:
                l = [a[idx[j]] for j in range(len(idx))]
                z = np.zeros(num_cols + 1)
                z[:len(idx)] = l
                new_array = np.zeros(num_cols)
                j = 0
                k = 0
                while j < num_cols:
                    val = z[j]
                    if val == z[j + 1]:
                        # Do merge
                        val = val * 2
                        # Increment score
                        swipe_score += val
                        j += 1
                    new_array[k] = val
                    j += 1
                    k += 1
                    board[:, i] = new_array

                if not np.array_equiv(a, new_array):
                    changed = True

        board = np.rot90(board, -Game2048.rot_dict[direction])

        return board, swipe_score, changed

    def swipe(self, direction):
        if not self.running:
            return

        if direction not in Game2048.valid_inputs:
            return

        board, swipe_score, changed = self._do_swipe(direction)

        # Rotate the board back
        self.board = board

        if changed:
            # Generate a new block in a random location
            nz = [(x[0], x[1]) for x in np.transpose(np.nonzero(self.board))]

            rows = self.board.shape[0]
            cols = self.board.shape[1]
            a = []
            for i in range(rows):
                for j in range(cols):
                    if (i, j) not in nz:
                        a.append((i, j))

            pos = np.random.choice(len(a), 1, replace=False)
            val = np.random.choice([2, 4], 1, replace=False)
            self.board[a[pos[0]]] = val

        self.score += swipe_score

        # Check if the board is full
        if np.count_nonzero(self.board) == np.prod(self.board.shape):
            changed = False
            for d in Game2048.valid_inputs:
                _, _, changed = self._do_swipe(d)
                if changed:
                    break

            # If no swipe direction changes the board then the game is over
            if not changed:
                self.running = False

        return swipe_score


if __name__ == '__main__':
    game = Game2048()
    while game.running:
        print(game, end='\r', flush=True)
        print(game.state)
        input_direction = input()
        game.swipe(input_direction)
    print("Game Over. Final Score:", game.score)
