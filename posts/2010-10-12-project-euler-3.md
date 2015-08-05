---
title: Project Euler 3 in c#
author: Adam Bell
tags: euler, c#
---
> Problem 3: What is the largest prime factor of the number 600851475143 ?
>
> [http://projecteuler.net/index.php?section=problems&id=3](http://projecteuler.net/index.php?section=problems&id=3 "http://projecteuler.net/index.php?section=problems&id=3")

With enough extension methods we can make 3 really simple:

> 600851475143.LargestPrimeFactor()

Where:

``` csharp
public static int LargestPrimeFactor(this long number)
{
    return number.PrimeFactors().Last();
}

public static IEnumerable<int> PrimeFactors(this long number)
{
    long remainder = number;
    while (true)
    {
        var factor = remainder.SmallestPrimeFactor();
        yield return factor;
        remainder = remainder / factor;
        if (remainder == 1)
        {
            break;
        }
    }
}

private static int SmallestPrimeFactor(this long number)
{
    var primes = new Eratosthenes();
    var factor = primes.FirstOrDefault(x => number.IsDivisbleBy((long)x));
    if (factor == 0)
    {
        throw new Exception(String.Format(“Factor not found! {0}”,number));
    }
    return factor;
}
```
