
<!-- image -->
<div align="center" id="top"> 
  <img src=images/model.png width="250" />
  <img src=images/real1.jpg width="177" />
  <img src=images/real2.jpg width="156" />
  &#xa0;
</div>

<h1 align="center"> robotic-connect-four </h1>
<h2 align="center"> Robotic connect four game - play against robot !
 </h2>

<!-- https://shields.io/ -->
<p align="center">
  <img alt="Top language" src="https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python">
  <img alt="Status" src="https://img.shields.io/badge/Status-In Progress-red?style=for-the-badge">
  <img alt="Repository size" src="https://img.shields.io/github/languages/code-size/KamilGos/robotic-connect-four?style=for-the-badge">
</p>

<!-- table of contents -->
<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0;
  <a href="#package-content">Content</a> &#xa0; | &#xa0;
  <a href="#microscope-tests">Tests</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#technologist-author">Author</a> &#xa0; | &#xa0;
</p>

<br>

## :dart: About ##
Connect four (also known as Four in line, Four Up, Plot Four, Find Four, Captain's Mistress, Four in a Row) is a two-player connection board game, in which the players choose a colour and then take turns dropping coloured discs into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.

The idea behind this project was to modify this game by adding a robotic player, which makes it possible to play human vs robot. The robot is controlled using the heuristic algorithm, so its movements are human-like.

Main assumptions: This project breaks with the two-player principle. One of the players is to be a computer. Image processing and algorithms derived from the theory of the game will be applied. The game will start after the user selects one of the difficulty levels on the control panel. The entire game process will follow traditional rules. One game lasts up to a few minutes. Movement from "artificial intelligence" will take place with the use of a specially designed mechanism, which is based on a stepper motor, servos and a gripper. The Raspberry Pi will be used in this project.

## :package: Content
 * [CAD](CAD) - STEP file with presented model
 * [main.py](main.py), [sources](sources) - implementation of algorithms responsible for executing the whole game
 * [utils](utils) - some additional scripth helpfull for adjusting the game

## :microscope: Tests ##
So far, several tests of the algorithm and mechanics control have been carried out, which indicate that the project will be successful. The last step is to generate the commands to control the servo motors and connect all togoether.

## :memo: License ##

This project is under license from MIT.

## :technologist: Author ##

Made with :heart: by <a href="https://github.com/KamilGos" target="_blank">Kamil Goś</a>

&#xa0;

<a href="#top">Back to top</a>
