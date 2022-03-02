from envs.env_two_player import TwoPlayerEnv

class SinglePlayerEnv(TwoPlayerEnv):

    def __init__(self, agent2):
        super().__init__()
        self.agent2 = agent2

    def reset(self):
        self.last_obs = super().reset()
        self.last_done = False
        return self.last_obs

    def step(self, action):
        self.pygame.do_action(action)
        reward = self.pygame.evaluate()
        self.last_done = self.pygame.is_done()

        if self.pygame.error > 0 or self.last_done: # There is an error, the move could not be played or the game has ended
            self.last_reward = reward
        else: # The move was played so we make the opponent play
            player_opponent = self.pygame.board.currentPlayer
            obs = self.pygame.observe()
            while self.pygame.board.currentPlayer == player_opponent:
                action = self.agent2.getAction(self, obs)

                # if the action is valid we play it in the env
                if action < 81: self.pygame.do_action(action)

            self.last_obs = self.pygame.observe()
            reward2 = self.pygame.evaluate()
            self.last_done = self.pygame.is_done()

            # Here we return as the reward the reward of the agent move - the reward of his opponent for his move
            self.last_reward = reward + reward2

        return self.last_obs, self.last_reward, self.last_done, self.pygame.error