---
title: Incrementing
author: Adam Bell
tags: paul-graham, haskell
---

In [an old essay](http://www.paulgraham.com/icad.html), Paul Graham, talks about how some languages are more succinct and therefore they are more powerful. In fact, some programming languages can say things that you can’t easily say in others. Maybe you can’t say them at all. Its a good essay overall, you should read it.

His Example:

> Write a function that takes a number n, and returns a function that takes another number i and returns n incremented by i.

I think this example is, maybe, unfairly biased towards functional programming languages, and its no surprise that pg shows us that lisp has the shortest implementation.

It works as a good example, however, because it shows us a concrete demonstration where one language can easily do something (lisp), that others languages are not able to do at all (java).

Let me try this in haskell.

So in Haskell, the type of this function f would be:

> f :: Num a => a -> ( a -> a)

meaning f takes a number and returns a function that takes a number and returns another number.

Since the brackets are right associative, we can drop them to get:

> f :: Num a => a -> a -> a

This is because, in haskell, all functions are considered curried and can be partially applied. Even basic numerical functions like + - / if given one argument will return a function that excepts the next argument.

For example:

> >:t (+)
>
> (+) :: Num a => a -> a -> a
>
> >:t (+) 4  
> (+) 4 :: Num a => a -> a

So (+) 4 returns a function that takes a number and then adds 4 for to it.
(_I mean, I guess technically, it doesn’t add 4 to it, but returns a new number that is the sum of them, but I think I am still capturing the spirit of the exercise here. Haskell variables are not mutable.)  
_

What all of this means, if I haven’t already telegraphed the punchline, is that the complete haskell solution is:

> f = (+)

So, in haskell, we don’t need to write this function. We can just use +.

I think that is pretty cool.
