# Charles Cook's Icosahedron Generator
## A Mathematical Python Script

### Begun April 23rd, 2019
### UV Map Added April 20th, 2021
### Handed-ness Correction Added April 21st, 2021

## Description

[orbit]: ITSBACK.gif
[heli]: manymanyicosahedra.gif
[uv1]: UVNotes1.jpg
[uv2]: UVNotes2.jpg
[finished]: result.jpg

An icosahedron is the largest of the five Platonic Solids (by face count).
It captivated me when I was taking my first Computer Graphics course due to my use of it as a 20 sided die, or d20 as it is known, in my long-running D&D sessions with friends.
Thus, I wanted to make a perfect representation of it in digital form.

Originally, I just wanted the shape itself, which required defining its vertices and faces, with the later requiring vertex-triplets and normal vectors.
I was able to accomplish this in short order, and produced the following animations via OpenGL in C++:

![Orbiting][orbit]
![SO YOU REALL WANNA KNOW? double;;double;;][heli]

Two years passed, and I wanted to use it again in a VR video game project.
It imported into Unity just fine, but I remembered I didn't give it a proper UV map back in the day.
Thus, I set about drawing one out on paper, using the existing and fixed real vertices to stitch it correctly onto the model:

![][uv1]

After some fine tuning, I was able to map the UV vertices to their Real counterparts with some set arithmetic, and all looked well, except it seemed a dice texture I applied seemed mirrored.

It was at this point I read a bit more about the file format I was using, Wavefront OBJ, and realized that it's a right handed coordinate system;
With how I had drawn the slices of the icosahedron to map UV vertices to Real vertices, I was using a left handed coordinate system.
Without getting to more into what all that means, to fix it I simply had to redraw the slices, this time with the z-axis pointing down (not up), and redo my relations, and ...

![][uv2]

After many off-by-one errors, it worked.
To understand the full algorithm, I leave as an exercise to the reader to follow the carefully commented code, along with running the program for yourself.

![][finished]
