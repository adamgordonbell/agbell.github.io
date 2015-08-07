---
title: Problems Clojure thinks I have with C#
author: Adam Bell
tags: clojure, c#
---
I am reading “Joy Of Clojure”. It seems like a good book, but it keeps telling me about these problems I have which I don’t percieve as problems.
<!--more-->
I’m not looking for Clojure to save me from these “problems” I just started playing with it because of some Rich Hickey talks that made me think there was a better way to develop software.

## Problems:

### Order of operations

Prefix notation is simpler, but order of operations have never been a big problem in my programming life.

### The Expression Problem

_[http://en.wikipedia.org/wiki/Expression_problem](http://en.wikipedia.org/wiki/Expression_problem)_

Protocols seem cool. But C# has extension methods, so adding a method to a class after the fact is no problem and the namespace scoping of extension methods avoids most monkey patching problems

### Concurrency

Ok, this is a big one, and making concurrency easier would be a big win for a lot of people. But not for me. I build web apps, I haven’t kicked off a bunch of threads in a long time.