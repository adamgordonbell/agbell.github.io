---
title: Introducing Attribute Based Caching
author: Adam Bell
tags: c#, attribute-based-caching
---
> “There are only two hard problems in computer science: cache invalidation, naming things, and off-by-one errors.”

I am a big fan of postsharp and its creator Gael.  There are a number of examples floating around of doing [caching](http://johnnycoder.com/blog/2009/01/16/caching-with-c-aop-and-postsharp/ "caching") with postsharp.  However, none handled cache invalidation in a nice declarative way.  

<!--more-->

I have released a caching library that uses [postsharp](http://www.sharpcrafters.com "Postsharp") on codeplex.  

[](http://cache.codeplex.com/ "http://cache.codeplex.com/")**[http://cache.codeplex.com/](http://cache.codeplex.com/)**  

It has some neat attribute based cache invalidation features and can use an in-memory cache or velocity.


(Options include In-process and Out-Of-Process and Off. Out-Of-Process uses Microsoft ApplicationServer.Caching)
*   Declarative Caching & Declarative Cache Invalidation ( use method name or configurable “GroupName” plus method parameters to cache & trigger cache invalidation)

### Simple Example( No invalidation):

> [Cache.Cacheable] //this method now cached, will only be called once per guid  
> public SomeExpensiveObject GetExpensiveObject(Guid userId)  
> {  
>  ..  
> }

### Full Featured Example:

> <pre><span>using</span> System;  
> <span>using</span> System.Collections.Generic;  
> <span>using</span> System.Linq;  
> <span>using</span> System.Text;  
> <span>using</span> CacheAspect.Attributes;  
>
> <span>namespace</span> TestCache  
> {  
>     <span>class</span> <span>UserRepository</span>  
>     {  
>         <span>//Get All Users is cached in Key = "GetAllUsers"</span>  
>         [<span>Cache</span>.<span>Cacheable</span>(<span>"GetAllUsers"</span>)]   
>         <span>List</span><<span>User</span>> GetAllUsers()  
>         {  
>             ...  
>         }  
>
>         <span>//GetUserById is cached using "GetUserById" + ID parameter</span>  
>         [<span>Cache</span>.<span>Cacheable</span>(<span>"GetUserById"</span>)]  
>         <span>User</span> GetUserById(<span>int</span> Id)  
>         {  
>             ...  
>         }  
>
>         <span>//Add user invalidates "GetAllUsers" cache key (User parameter is ignored)</span>  
>         [<span>Cache</span>.<span>TriggerInvalidation</span>(<span>"GetAllUsers"</span>, <span>CacheSettings</span>.IgnoreParameters)]  
>         <span>void</span> AddUser(<span>User</span> user)  
>         {  
>
>         }  
>
>         <span>//Delete user invalidates both GetAllUsers & GetUserById</span>  
>         <span>//The user parameters Id property is used to build Key for "GetUserById"+ Id  Key</span>  
>         <span>//this is done using a bit reflection</span>  
>         [<span>Cache</span>.<span>TriggerInvalidation</span>(<span>"GetAllUsers"</span>, <span>CacheSettings</span>.IgnoreParameters)]  
>         [<span>Cache</span>.<span>TriggerInvalidation</span>(<span>"GetUserById"</span>, <span>CacheSettings</span>.UseId)]  
>         <span>void</span> DeleteUser(<span>User</span> user)  
>         {  
>             ...  
>         }  
>         
>     }  
> }  
> </pre>

[http://cache.codeplex.com/SourceControl/changeset/view/1505#25143](http://cache.codeplex.com/SourceControl/changeset/view/1505#25143 "example") <span> </span>

This example shows how an expensive object (user in this case) might be cached at the repository level.  It shows how attributes can be used to clear from the cache stale objects based on add update and delete changes in a declarative fashion. 

Please excuse the empty method bodies for now.  I will have a better sample project put together at some point.
