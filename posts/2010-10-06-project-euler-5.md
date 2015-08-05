---
title: Project Euler #5
author: Adam Bell
tags: euler, c#
---
Here is my solution to the following project Euler Problem:

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

http://projecteuler.net/index.php?section=problems&id=5
```
 int result =
    (
        from a in Multiples.Of(20)
        where a.IsDivisbleBy(19.To(2))
        select a
    ).FirstOrDefault();
```
Where:
```
static class Multiples
{
    public static IEnumerable<int> Of(int n)
    {
        return from i in 1.To(Int32.MaxValue / n)
                select i * n;
    }
}
```
And:
```
public static bool IsDivisbleBy(this int x, IEnumerable<int> range)
{
    foreach (int i in range)
    {
        if (!x.IsDivisbleBy(i))
        {
            return false;
        }
    }
    return true;
}

public static bool IsDivisbleBy(this int x, int y)
{
    return x % y == 0;
}

```
