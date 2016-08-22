---
title: Modifier Keys in the Home Row
author: Adam Bell
tags: keyboard, ergodox
---
![](/images/keyboard-layout_ergodox.png)
With today's opensource keyboard firmware, it is possible to use dual role keys to have all modifier keys in your home row.
<!--more-->

I don't like having to leave the home row on the keyboard enter commands like CTRL-S or even CTRL-ALT-Left Arrow.  Using the tmk firmware or ( the qmk fork) I am able to have my keys function as normal when pressed, but as a modifier when held down.

## [Dual-role keys:](https://en.wikipedia.org/wiki/Modifier_key#Dual-role_keys)
```

It is possible to use (with some utility software) one same key both as a normal key and as a modifier.

For example, you can use the space bar both as a normal Space bar and as a Shift. Intuitively, it'll be a Space when you want a whitespace, and a Shift when you want it to act as a shift. I.e. when you simply press and release it, it is the usual space, but when you press other keys, say X, Y and Z, while holding down the space, then they will be treated as ⇧ Shift plus X, Y and Z.

The above example is known as "SandS", standing for "Space and Shift" in Japan. But any number of any combinations are possible.

To press shift+space in the previous example, you need in addition to a space/shift dual role key, one of (a) another space/shift key, (b) a usual shift, or (c) a usual space key.
-- Wikipedia

```

In my keymap, D and K when held down act as Ctrl, L and S do the same for Alt.  Shift is placed under A and ;.  Additionally, F or J active a layer with F1-F12 as well as some extra keys (~/|?\) and arrow keys under my right hand.  My Escape key also acts as the windows key if held down.  It sounds complicated, but the muscle memory takes over after an hour or two and it just feels fast and simple.

Resources:

 * [My keymap for the ergodox keyboard](https://github.com/agbell/tmk_keyboard/blob/cub_layout/keyboard/ergodox/keymap_adam.hs)
 * [TMK firmware](https://github.com/tmk/tmk_keyboard)
 * [QMK firmware](https://github.com/jackhumbert/qmk_firmwares)
