---
title: WordPress Force “View all posts in %s” for categories
author: Adam Bell
tags: wordpress
---
Force categories list not to use category descritption use this:


```

      $args\_list = array(

     ‘use\_desc\_for\_title’ => 0

      );

      $list = wp\_list\_categories( $args\_list );

```
