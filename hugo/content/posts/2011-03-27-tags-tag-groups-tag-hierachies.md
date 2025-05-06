---
title: "Incrementing"
author: "Adam Bell"
date: 2011-03-27
tags: [tags, data]
---
_Generic Hierarchical Meta data is cool! There are many ways to implement it with a standard relational database. Most of them are considered anti-patterns, but sometimes we need to optimize for flexibility, not raw database performance. Here are some of my notes on the subject:_
<!--more-->
If all entities in the system can contain a list of tags, and the tagging system is structured correctly, the following features can be supported:

* [faceted search](http://en.wikipedia.org/wiki/Faceted_search)
* hierarchical organization (categories, sub-cats and so on represented in tag hierarchy)
* ordering entities (‘high priority tag")

This should allow for a flexible meta-data system over top of the entities which can be customized with very little code modifications.

This can be accomplished by having a tag tree, where tag entities have the following fields:

* Name
* ParentId
* Weight
* Hierarchy Path (for sub-tree searches)
* Shortcut

The following tag search can then be implemented in SQL:

* And search (tag X and tag y)
* Or Search
* Except search
* Sub-tree inclusive or not

Assuming that most tag trees are only 2 levels deep and using a subtree inclusive search when this is not the case (or always), we treat each tag tree as a facet in a faceted search.

A hierarchy of categories and sub categories can be built by building the tag hierarchy and assigning all items into leaf tags and once again using an inclusive tag search as we drill down.

If tags in a tree are given weights, entities can be sorted by these tags in , for instance, a grid.

Tag Input:

* specify path example: facet1/tag1, color/red
* User shortcuts to aid entering new tag {name=“color”,shortcut=“#c”}, then can be used like #c/red

**Other considerations:**

**Null Tag :**

Null tag could be added to any subtree which would catch all entities without a tag in that tree. This would be helpful for facet navigation and search.

**_Null tag for facet:_**

A null tag of “Unknown color” could be added as a child of the color tag, and would return all entities without a color tag.

_**Null tag for sorting:**_

A null tag of “no priority” could be added as a child of the priority tag and be given a weight of zero, hence sorting on this priority tag tree would return un-prioritized entities last.

**Need cohesive example. Another Post.**

**Tagging Links:**

* [How to Make a Faceted Classification and Put It On the Web | Miskatonic University Press](http://www.miskatonic.org/library/facet-web-howto.html)

* [Faceted classification - Wikipedia, the free encyclopedia](http://en.wikipedia.org/wiki/Faceted_classification)

* [Collection: Faceted Navigation](http://www.flickr.com/photos/morville/collections/72157603789246885/)

* [Advanced Tagging — Hierarchical And Ordered Tags « PubNotes](http://pubnotes.wordpress.com/2007/10/14/ordered-tags/)

* [Advanced Tagging - Things Wiki](http://culturedcode.com/things/wiki/index.php?title=Advanced_Tagging)

**Tags as categories:**

* [http://www.znode.com/](http://www.znode.com/)

_Znode uses Tag groups to represent categories and to implement a faceted search. Their implementation is only 2 fixed levels however._
