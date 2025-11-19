# Gemini-3-Pro-Evaluations

## Introduction
Google released their state-of-the-art reasoning model, Gemini 3.0 Pro on 18th November, 2025. The model claims to have exceptional "vibe coding" capabilities. This was to a test against Google's own previous SOTA reasoning model, Gemini 2.5 Pro. The two models were tested against 5 coding tasks. It was also taken care that no excessive prompting was done (prompts were kept relatively simple) to keep the "vibe coding" spirit.

## Tasks

### First Task
The models were prompted to create a personal portfolio website with a tech aesthetic.

**Prompt:**
```
Create a tech-based personal portfolio site with minimalism in mind. Add a tech aesthetic to it, and keep the elements simple. Add various sections on the website to make it look appealing.
```

Though Gemini 2.5 Pro did a good job at creating the site, Gemini 3.0 Pro's response was phenomenal. This showed that Gemini 3.0 pro is better at implementation even with a simple prompt, likely to foster the "vibe coding" spirit.

### Second Task
The models were prompted to create a simple pixelated 2D Top-down RPG in Python using PyGame.

**Prompt:**
```
Create a top-down 2D pixelated RPG game in Python using PyGame.
```

Again, both the models were able to make the game, but Gemini 3.0 Pro's game had more of a purpose and playability, while Gemini 2.5 Pro's game looked incomplete and lacked purpose.

### Third Task
The models were prompted to create a Terminal Emulator on Java.

**Prompt:**
```
Write code for a basic terminal emulator program in Java. It should look and function as a normal terminal.
```

This time, Gemini 2.5 Pro's response was more functional. Gemini 3.0 Pro tried to implement better aesthetics, but failed to implement good functionality.

### Fourth Task
The models were prompted to create a Minecraft clone using PyGame.

**Prompt:**
```
Write code for a Minecraft clone using PyGame. No external assets will be provided.
```

Gemini 2.5 Pro failed to understand the point of the prompt and went ahead and created an isometric clone of Minecraft. Gemini 3.0 Pro actually implemented OpenGL rendering and created a 3D game with basic controls.

### Fifth Task
The models were prompted to create a Fully-Fledged Rich Text Editor in C++.

**Prompt:**
```
Write C++ code for a fully-fledged rich-text editor which has all the necessary features a rich-text editor like Google Docs should have.
```

This was probably the most complex task out of the five. Neither of the models were able to create a working program in the first prompt. They made it work after the 3rd-4th prompt though. Gemini 3.0 Pro's product looks a bit more fleshed out, while Gemini 2.5 Pro's is more barebones.

## Conclusion
It is clear that Gemini 3.0 Pro is a cut above its predecessor, with better "vibe coding" capabilities and abilities to implement necessary features from a simple prompt. It also is better at implementing aesthetics.