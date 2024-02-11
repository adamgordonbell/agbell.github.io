---
title: Enterprise Software Authorization / Security
author: Adam Bell
tags: row-level-authorization, field-level-authorization
---
![lock](http://media.tumblr.com/tumblr_lcz5n7fN1g1qdwslz.png)**Security Thoughts:**

There are generally three types of authorization in enterprise applications:

1. <span><span></span></span>**Role based security** **-** Which actions can a user do - aka role-based access control<span><span></span></span>
2. <span><span></span></span>**Entity level security** - A user can only perform an Action on certain objects/data - aka row level security
3. **Field level security** - A user can see or edit only certain fields of an entity – _(this is really fine grained and usually a bad idea)_

<!--more-->

There is a framework that covers all 3 of these authorization types, Rhino Security. It allows authorization to be abstracted from the business logic as a cross-cutting concern. It is deigned to handle 1 & 2 above, but people have used it to implement 3\.

Here is an example of the type of rules it can easily encompass:

> Survey Entity:
>
> A survey has a start date, an end date, can be marked as applicable to a specific population, may be public or private, etc.
>
> View Restrictions:
>
> The specification says that a survey that the user does not own should only be visible to a user iff:
>
> * The survey is public
> * The survey is active
> * The survey has started
> * The survey has not ended
> * The survey is for a population that the user is a member of
>
> [http://ayende.com/Blog/archive/2009/12/11/handling-complex-security-conditions-with-rhino-security.aspx](http://ayende.com/Blog/archive/2009/12/11/handling-complex-security-conditions-with-rhino-security.aspx)

**Entity Group:**

The key concept that separates it from standard role based security is the concept of an entity-group. Entity groups are group of, well, entities and users can be granted/denied access to them just like actions.

I would really love to see someone port this concept to the entity framework. It certainly might not be right for every project, but a cohesive strategy for access control would be a big leap forward compared to a lot of projects I’ve worked on.

**Further Reading:**

* [Handling complex security conditions with Rhino Security](http://ayende.com/Blog/archive/2009/12/11/handling-complex-security-conditions-with-rhino-security.aspx "Title of this entry.")
* [Field level security performance with Rhino Security](http://bartreyserhove.blogspot.com/search/label/rhino%20security)
* [Rhino Security](http://ayende.com/Blog/category/548.aspx)
* [A vision of enterprise platform Security Infrastructure](http://ayende.com/Blog/archive/2007/11/17/A-vision-of-enterprise-platform-Security-Infrastructure.aspx)
* [Rhino Security Overview](http://ayende.com/Blog/archive/2008/01/22/Rhino-Security-Overview-Part-I.aspx)
