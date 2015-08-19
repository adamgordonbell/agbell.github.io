---
title: More Scala Groups And Tuples
author: Adam Bell
tags: scala, slick, tuples
---

Continuing from [here](http://cascadeofinsights.com/posts/2015-08-04-scala-slick-group-joins.html), I have lists of tuples and I want to group them.  Here I have a list of 4-tuples and I want to group the second tuple by the first.  *The fact that I need to do this probably represents some greater problem, but that is a story for another time*  

``` scala
import shapeless._
import syntax.std.tuple._
import poly._

object GroupLists {
def group1TwoExtra[A,B,C,D](t : List[(A,B,C,D)]) : List[(A,List[B],C,D)] = {
      val map = LinkedHashMap[A, LinkedHashSet[B]]()
      val mapOther = scala.collection.mutable.Map[A,(C,D)]()
      for (i <- t) {
        val key = i.head
        map(key) = map.lift(key).getOrElse(LinkedHashSet[B]()) + i.drop(1).head
        mapOther += (key -> i.drop(2))
      }
      map.map(b => (b._1, b._2.toList) ++ mapOther(b._1)).toList
    }
```
<!--more-->
That was easy.  The use of head and drop from shapeless lets you act on tuples like they are lists.  However abstracting away the size of the tuples gets tricky, because we need type annotations to make the compiler happy.  

Here is the same implementation for 5-tuples:
``` scala

def group1ThreeExtra[A,B,C,D,E](t : List[(A,B,C,D,E)]) : List[(A,List[B],C,D,E)] = {
      val map = LinkedHashMap[A, LinkedHashSet[B]]()
      val mapOther = scala.collection.mutable.Map[A,(C,D,E)]()
      for (i <- t) {
        val key = i.head
        map(key) = map.lift(key).getOrElse(LinkedHashSet[B]()) + i.drop(1).head
        mapOther += (key -> i.drop(2))
      }
      map.map(b => (b._1, b._2.toList) ++ mapOther(b._1)).toList
    }

```
The interesting thing here is that, except for type annotations, these definitions are exactly the same.

To be continued...
