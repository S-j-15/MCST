Hey Hey...so in this repo... I implemented Monte Carlo Tree Search (MCTS) from scratch in python...yeah...
so basically how it works is you play a move it makes a game state...the MCTS funs for N iterations...where it selects a node in already existing tree based on pinciple of exploration and exploitation:
its given by the formula:
<img width="328" height="77" alt="image" src="https://github.com/user-attachments/assets/3fb8e886-a7b1-4629-8c00-16740103e40e" />
so basically choose the best child... then expand on it...we run random simulation on it (rollout) and finally see which node has like the maximum number of visits in all the iterations...then give that game state as the best move

here is a sample output of me losing on purpose (DONT U DARE CALL ME A NOOB >:(! )

<img width="314" height="658" alt="image" src="https://github.com/user-attachments/assets/47eabcf0-5de1-45c1-a932-9f14108cd6ae" />

Thank You

