---
title: Code Generators, You Suck. Well, some of you do.
author: Adam Bell
tags: wssf
---

The scaffolding style code generators that generate out a good starting point from which standard coding takes over, those are very useful.

The Microsoft brand “design surface” based code generators (TableAdapters,[WSSF](http://servicefactory.codeplex.com)) where the uml diagram of a class needs to be edited, rather than the actual class, those are more harm than good. if fact they slow development way down.

The design surface itself, is not necessarily a bad concept. it is just a GUI over top of a XML document. Just don’t use it to generate repetitive code. If code is repetitive, factor it out until its DRY. Don’t break out the code generators.
