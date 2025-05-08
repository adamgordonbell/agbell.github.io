---
title: "Lazy Evaluation In Haskell"
author: "Adam Bell"
date: 2015-01-14
tags: []
---
_This post is a work in progress and represents my getting to understand how laziness works in haskell and how it affects performance._
<!--more-->
Summary of Laziness:

Lazy is good when:

* You are not going to use all the results
* Because you are going to filter some things out at a later stage

Strict is good otherwise.  
Hence:

* foldl’ for spine-strict results (Int, Map, …),
* foldr for spine-lazy results (mostly just [a]),
* Never use foldl

The key insight for me has been understanding that lazy evaluation means that functions take in a pointer to a thunk as arguments and then return a thunk as a value. Only looking inside those thunks inputs (via pattern matching or IO) actually forces anything.

This level of indirection improves composability, you can generate than reduce in a more modular fashion with only some constant overhead for holding on to thunks. The paper “why functional programming matters” has a great explanation of this.

This all works because whenever you throw something away with _i.e. f (a,_) = a, the pointer to the thunk, that was never evaluated, and all the evaluations that follow from can get garbage collected away.

This how foldr can short-circuit on some lazy list, if a condition of f that is passed in doesn’t care about the rest of the list, then we are done.

<span>Links:</span>

* [Ez Yang : how the heap works](http://blog.ezyang.com/category/haskell/haskell-heap/)
* [http://www.haskellforall.com/2014/10/how-to-desugar-haskell-code.html](http://www.haskellforall.com/2014/10/how-to-desugar-haskell-code.html)
* [http://www.haskell.org/haskellwiki/Performance/Strictness](http://www.haskell.org/haskellwiki/Performance/Strictness)
* [http://en.wikibooks.org/wiki/Haskell/Laziness](http://en.wikibooks.org/wiki/Haskell/Laziness)
* [http://en.wikibooks.org/wiki/Haskell/Laziness#Black-box_strictness_analysis](http://en.wikibooks.org/wiki/Haskell/Laziness#Black-box_strictness_analysis)
