---
title: "Project Euler #6"
author: "Adam Bell"
date: 2010-10-06
tags: [euler, c#]
---
Ok, this one is stupidly simple:

```
var squaredsum = Math.Pow(1.To(100).Sum(), 2);
var sumedsquare = 1.To(100).Select(x => x * x).Sum();
Console.WriteLine(squaredsum - sumedsquare);

```
