# UltimateTicTacToe-RL

The goal is to design an AI using RL to play Ultimate Tic Tac Toe.

See the paper to learn the rules.

## Requirements
```pip install pygame```

```pip install numpy```

```pip install time```

```pip install gym```

```pip install torchvision```

## How to launch

You need to launch from the root of the folder the scripts in **play_modes**.

You can use **agent_in_single_player_env.py** to make 2 agent fight each other (one of them can be you).

The best agent is **MinimaxPruningAgentSeveralRewards** so try to beat him!

<br/>

**WARNING: You may experience some path issues. To solve this simply add the absolute path of this folder in the script like so**
```
import sys
sys.path.append("C:\\Users\\Marie\\Organisation_Marie\\X\\3A\\INF 581 - Advanced machine learning\\Project\\UltimateTicTacToe-RL")
```
Enjoy !


## How to recreate the results presented in the paper

You can launch **play_modes/stats.py** to make each agent fight against each other for several games in order to get statistics. However, this process takes dozen of hours so you need to be patient. To then visualize the figure presented in the paper, you can then use **display_results.py** with the values printed by the previous script.

