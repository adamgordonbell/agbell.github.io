---
title: "Project Euler #24 in c#"
author: "Adam Bell"
date: 2010-11-11
tags: [euler, c#]
---


A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4\. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

<!--more-->

``` csharp
[TestClass]
    public class Problem24
    {
        [TestMethod]
        public void Answer()
        {
            var tokens = new string[] { “0”, “1”, “2”, “3”, “4”, “5”, “6”, “7”, “8”, “9” };
            var results = Permutations.Of(tokens).WithLength(10);
            results
                .Skip(999999)
                .Take(1)
                .ToList()
                .ForEach(x => Console.WriteLine(x));
            Console.ReadLine();
        }
    }

public class Permutations
    {
        public static Permutations Of(IEnumerable<string> tokens)
        {
            return new Permutations { tokens = tokens.ToList() };
        }
        private Permutations() { }

        public IList<string> tokens { get; private set; }

        public IEnumerable<String> WithLength(int length)
        {
            if (length < 1 || length > tokens.Count())
            {
                return null;
            }
            if (length == 1)
            {
                return tokens.Select(x => x);
            }
            var results = from t in tokens
                          from x in Permutations.Of(tokens.RemoveWithCopy<String>(t)).WithLength(length - 1)
                          select t + x; //this is using string builder
            return results;
        }
    }
```
