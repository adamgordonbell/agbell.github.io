---
title: "Scala Slick Group"
author: "Adam"
date: 2015-08-04
tags: [scala, slick]
---
In slick, if each foo has many bars and I need to retrive several foos and associtated bars I will do something like this:

``` scala
val join = for {
     (f,b) <-
                  foo.filter(...) on  innerJoin
                  bar on (...)
   } yield (o,i,s)
```
<!--more-->

The type of join will be a List[(foo,bar)].  I want the bars grouped by foo, not a tuple of each. I can transform to a grouped format like so:

``` scala
def group1[A,B](t : List[(A,B)]) : List[(A,List[B])] = {
    val map = LinkedHashMap[A, LinkedHashSet[B]]()
    for (i <- t) {
      val key = i._1
      map(key) = map.lift(key).getOrElse(LinkedHashSet[B]()) + i._2
    }
    map.map(b => (b._1,b._2.toList)).toList
  }
```

This groups one element from a tuple into a sublist.  If I later add the requirement that each bar has many baz than I need to another method that transforms tuples of 3 into two nested lists.

``` scala

def group2[A,B,C](t : List[(A,B,C)]) : List[(A,List[(B,List[C])])] = {
    group2Internal(t).map(x => (x._1,group1(x._2)))
  }

private def group2Internal[A,B,C](t : List[(A,B,C)]) : List[(A,List[(B,C)])] = {
   val map = LinkedHashMap[A, LinkedHashSet[(B,C)]]()
   for (i <- t) {
     val key = i._1
     map(key) = map.lift(key).getOrElse(LinkedHashSet[(B,C)]()) + ((i._2,i._3))
   }
   map.map(b => (b._1,b._2.toList)).toList
 }

```

I can do the same for grouping into three nested lists:

``` scala
def group3[A,B,C,D](t : List[(A,B,C,D)]) : List[(A,List[(B,List[(C,List[D])])])] = {
    group3Internal(t).map(x => (x._1,group2(x._2)))
}

private def group3Internal[A,B,C,D](t : List[(A,B,C,D)]) : List[(A,List[(B,C,D)])] = {
   val map = LinkedHashMap[A, LinkedHashSet[(B,C,D)]]()
   for (i <- t) {
     val key = i._1
     map(key) = map.lift(key).getOrElse(LinkedHashSet[(B,C,D)]()) + ((i._2,i._3,i._4))
   }
   map.map(b => (b._1,b._2.toList)).toList
 }

```

There is obviously a pattern here that should be abstractable.  However, at the type level, tuples of different sizes are unqiue types, so this gets tricky.  It should be possible to use the [shapeless](https://github.com/milessabin/shapeless) library to abstract over the tuple size.  In practice I never need more than group3, so this will stay in its expanded form for now.
