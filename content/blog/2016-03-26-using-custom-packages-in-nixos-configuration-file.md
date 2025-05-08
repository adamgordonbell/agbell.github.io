---
title: "Using Custom Packages in NixOs Configuration File"
author: "Adam Bell"
date: 2016-03-26
tags: [nix, nixos]
---

Here is a problem we encountered with NixOS:

The nix-channel we were on didn't have the latest version of something we needed. This happened recently when my coworker upgraded to Postgres 9.5 from 9.4 but the PostGIS version in nixpkgs hadn’t been updated to a 9.5 compatible version.
<!--more-->

### Upgrading Nix Package PostGIS

*same steps apply for any package*

* fork nixpkgs in GitHub
* updated nix package for PostGIS
* built it
* [submitted as a pull request to nixpkgs](https://github.com/NixOS/nixpkgs/pull/13572/commits/c267f5b71122453268d55ef665f20262be7f53d9)

### Including package in configuration.nix

If this package were a stand-alone program, we could have installed it from our forked pkgs. However, this package is referenced in a service that is configured globally in NixOS so we needed to be able to reference our forked package repo in our configuration.nix file.

*If we were on the unstable channel the package would have eventually shown up, when our pull request was merged in and when the channel is updated from Github. However, we couldn't wait for that.*

### Referencing our fork of nixpkgs in our configuration.nix

We created a reference to our forked packages using a let expression in our configuration.nix file.  This allowed us to globally reference packages both from the channel we are subscribed and from our custompkgs fork.

Using a let expression, we pulled in our fork of nixpkgs:

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
