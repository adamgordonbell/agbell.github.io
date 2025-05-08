---
title: "WordPress Force “View all posts in %s” for categories"
author: "Adam Bell"
date: 2012-07-15
tags: [wordpress]
---
Force categories list not to use category descritption use this:
<!--more-->

```

      $args\_list = array(

     ‘use\_desc\_for\_title’ => 0

      );

      $list = wp\_list\_categories( $args\_list );

```
