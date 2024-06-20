# manim-timeline: A Fun Recap of Literature Review! :tada:

This repository is meant to complement [manim-slides](https://github.com/jeertmans/manim-slides), and does not override it. 

The manim-timeline repository contains code that elegantly integrates historical events (such as philosopher's quotes or captioned images) 
with time-stamped publications as well as offer simple transitions to full-screen demos. This presentation mode is much more fun
and interactive than typical PowerPoint slides; it allows the presenter to provide historical context, rapid coverage of related work, 
and how this led to more recent advancements in the field of interest. manim-slides also utilizes [manim-beamer](https://github.com/johnHostetter/manim-beamer)
so intermittent slides on the timeline are styled similar to LaTeX Beamer for additional professionalism.

## Short Example of Timeline :eyes:
https://github.com/johnHostetter/manim-timeline/assets/35469358/9831fc2b-b51d-4942-9ab1-5b911b62ca52

## Real-World Example :bulb:
I used this code to propose my dissertation topic to my committee. I was able to provide a brief history of the field,
show how my work fits in, and then transition to a full-screen demo of my work. It was a hit! :tada:

Visit the slides for the full talk [here](https://jwhostetter.com/proposal/slides) 
(use Left and Right arrow keys to go backward and forward, respectively)! :rocket:

## Troubleshooting :worried:
- If you are having trouble with installing the `manim-beamer` package, please try the following:

  `
  python -m pip install git+https://github.com/johnHostetter/manim-beamer.git@main#egg=mbeamer
  `
