---
title: Naked Objects MVC - exposing a repository method as a get
author: Adam Bell
tags: c#, NakedObjectsFramework
---
If you would like to expose the results of an entity framework call as the index page or any other get based url using naked object mvc, a custom controller is required.
<!--more-->
``` csharp
public class HomeController : CustomController
    {
        public ActionResult Index()
        {
            var siteRep = FrameworkHelper.GetService<SimpleRepository<Site>>();
            return InvokeAction(siteRep, “All”, new FormCollection(), “”, “StandaloneTable”);
        }
    }
```
Here the home controller will return the StandaloneTable view of the All() method on SimpleRepository<Site>.
