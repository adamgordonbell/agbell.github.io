---
title: "Project Euler #9"
author: "Adam Bell"
date: 2010-10-07
tags: [c#, euler]
---
Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
<!--more-->
<http://projecteuler.net/index.php?section=problems&id=6>

My Solution:

```
var x =
    (
        from a in 1.To(Int32.MaxValue)
        from b in 1.To(a)
        where a + b + Math.Sqrt(a * a + b * b) == 1000
        select new { A = a, B = b, C = Math.Sqrt(a * a + b * b) }
    ).First();
```
