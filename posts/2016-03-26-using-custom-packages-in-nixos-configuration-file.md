---
title: Using Custom Packages in NixOs Configuration File
author: Adam Bell
tags: nix, nixos
---

Here is a problem we encounter with NixOS: The nix channel you are on doesn't have the latest version of something yet.  This happened recently when my coworker updated to postgres 9.5 but the postGIS version hadn't been updated to a 9.5 compatible version.
<!--more-->

### Upgrading Nix Package postgis:

*same steps apply for any package*

* fork nixpkgs in github
* updated nix package
* built it
* [submitted as pull request to nixpkgs](https://github.com/NixOS/nixpkgs/pull/13572/commits/c267f5b71122453268d55ef665f20262be7f53d9)

### Including package in configuration.nix:

If this package were a stand alone program, we could install it from our forked pkgs and be done with things.  However, if this package is a service or we would like to install it globally we have a small problem.  We need to reference this new package in the configuration.nix files, but it is not in channel we are subscribed to. If we are on the unstable channel the package will eventually show up, when our pull request in merged and when the channel is updated from github. However, who want to wait for that?  

### Referencing our fork of nixpkgs in our configuration.nix :
If we create a reference to our forked packages using a let expression in our configuration.nix file, we can globally reference packages both from the channel we are subscribed and from our custompkgs fork.

Using a let expression, pull in our fork of nixpkgs:

``` configuration.nix
{ config, pkgs, ... }:

let custompkgs = import /usr/local/nixpkgs/default.nix {}; in
{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];
    ....
```

``` configuration.nix
...
  services.postgresql = {
        enable = true;
        extraPlugins = [ (custompkgs.postgis.override { postgresql = pkgs.postgresql95; }).v_2_2_1 ];
    };
...
```
