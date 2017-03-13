# Corpse Stacker FAQ

https://github.com/serin-delaunay/corpsestacker

## What are the symbols on screen?

`@` is you. You should try to stay alive.

`z` is a zombie. It's not actively trying to kill you, but if it bumps into you it will.

`0123456789` are floor heights. Every time you kill a zombie, it becomes part of the pile of corpses on that tile.

## What am I trying to do?

Make a stack of 10 corpses.

## Why 10?

I only allotted one character to represent each tile's floor height.

## I'm trying to move to an adjacent space or attack a zombie and I can't!

You (and zombies) can only climb up 1 level or descend 3 levels in a single move. The same restrictions apply to attacking.

## I died!

It's a roguelike. Expect death.

## I made a plateau and none of the zombies can touch me now! Did I win?

No. You'll starve up there. Zombie meat is bad for you.

## How do zombies decide where to move?

They don't move to tiles at an illegal height.
They don't move to tiles containing another zombie.
They can move onto the tile you're standing in,
and that kills you.
They look at all four directions, eliminate impossible moves,
and randomly choose one from what remains.
If there are no legal moves, it skips its turn.

## How does spawning work?

As the maximum height increases from 0 to 9,
the expected number `E` of zombies per turn increases from 0.5 to 1.4.
Each turn either `floor(E)` or `ceiling(E)` zombies may spawn.
Each new zombie is placed on a random empty tile on the map border.
If there are no empty border tiles, the new zombie is not placed.

## I think this game is impossible to win.

This game can be won.
