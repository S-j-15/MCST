Hey Hey...so in this repo... I implemented Monte Carlo Tree Search (MCTS) from scratch in python...yeah...
so basically how it works is you play a move it makes a game state...the MCTS funs for N iterations...where it selects a node in already existing tree based on pinciple of exploration and exploitation:
its given by the formula:
<img width="328" height="77" alt="image" src="https://github.com/user-attachments/assets/3fb8e886-a7b1-4629-8c00-16740103e40e" />
so basically choose the best child... then expand on it...we run random simulation on it (rollout) and finally see which node has like the maximum number of visits in all the iterations...then give that game state as the best move

here is a sample output of me losing on purpose (DONT U DARE CALL ME A NOOB >:(! )

<img width="314" height="658" alt="image" src="https://github.com/user-attachments/assets/47eabcf0-5de1-45c1-a932-9f14108cd6ae" />

also i added like connect 4 using MCTS just had to make some changes to game state like new game new rules but the core idea is the same

also I suck at connect 4 :_(

<img width="1393" height="714" alt="Screenshot 2025-10-17 153607" src="https://github.com/user-attachments/assets/a402d9d3-759c-4cd0-a047-e4e58c9bf913" />



# mcts.py is for tic-tac-toe and mcts_with_gui is tic-tac-toe with GUI
# mcts_connect4 is for connect 4

Thank You

