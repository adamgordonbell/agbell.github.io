---
title: Using Custom Packages in NixOs Configuration File
author: Adam Bell
tags:
---

Here is a problem we encounter with NixOS.  The nix channel you are on doesn't have the latest version of something yet.  This happened recently when my coworker updated to postgres 9.5 but the postGIS version hadn't been updated to a 9.5 compatible version.
<!--more-->

Background:
forked this repo, updated package, built it and submitted as pull request to nixpkgs

Problems:
We need to reference this new package in the configuration.nix files, but it is not in channel we are subscribed to.

Solution:
Using a let experssion, pull in our fork of nixpkgs.

```

      $args\_list = array(

     ‘use\_desc\_for\_title’ => 0

      );

      $list = wp\_list\_categories( $args\_list );

```
