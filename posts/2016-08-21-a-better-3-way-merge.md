---
title: A Better 3-way merge?
author: Adam Bell
tags: git, merging, dummy_tag
---
3-way merge works great for code merges in the majority of cases.  Can we do better, however.  Can we decrease the number of places where a manual conflict resolution is required.  I would say, yes we can, if we know more about the syntax of the file in question.
<!--more-->

## An Example

### Base file:
``` scala
def x(a : string, b : Int) : Option[Int]
```

### Their file:
``` scala
def x(a : string, b : Int, c : String) : Option[Int]
```

### Our File:
``` scala
def x(a : string, b: Int, b2 : String) : Option[Int]
```

### Expected Result:
``` scala
def x(a : string, b: Int, b2 : String, c : String) : Option[Int]
```

The above will need to manually resolved in git, both branches makes change to the same line, so git does not know how to resolve this.  

However, if we had a similar merge, where the code was split across multiple lines, the 3-way merge would have no problem:


### Base file:
``` scala
def x(
  a : string
  ,b : Int
   ) : Option[Int]
```

### Their file:
``` scala
def x(
  a : string
  ,b : Int
  ,c : String
  ) : Option[Int]
```

### Our File:
``` scala
def x(
  a : string
  ,b: Int
  ,b2 : String
  ) : Option[Int]
```

### Result:
``` scala
def x(
  a : string
  ,b: Int
  ,b2 : String
  ,c  : String
  ) : Option[Int]
```
Thus we can see that by knowing where a line in a file can be split, we should be able to eliminate some merge conflicts.  If we wrote a bash script that called the default 3-way merge, and in cases of conflict, it introduced new lines everywhere possible based on the syntax rules of file and then called it again, before removing the introduced new lines, we would reduce the number of conflicts.  

It would handle our original case, by spreading the code across more lines, merging it and then recombining it.  We could then use that script as our custom merge driver.

Now I just have to write the thing and test it.  Stay tuned.
