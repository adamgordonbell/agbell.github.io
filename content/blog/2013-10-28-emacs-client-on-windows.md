---
title: "Emacs Client on Windows 8"
author: "Adam Bell"
date: 2013-10-28
tags: [emacs, windows]
---
Problem:

I want to use emacs like I use notepadd++ on windows.
<!--more-->
<span>That is:</span>

* Right click menu item to “edit with Emacs”
* Associate file types with emacs (like .org)
* Have only one emacs open at a time

Here are the steps I took:

1. Create the context menu like this ([global_context_emacs.reg](http://www.emacswiki.org/emacs/MsWindowsGlobalContextMenu)) :

    ```
    REGEDIT4
    [HKEY_CLASSES_ROOT\*\shell]

    [HKEY_CLASSES_ROOT\*\shell\openwemacs]
    @="&GNU Emacs"
    # The above value appears in the global context menu, # i.e., when you right click on a file.
    # (The '&' makes the next character a shortcut.) "Icon"="C:\\Program Files\\Emacs\\bin\\emacs.exe,0"
    # The above uses the icon of the Emacs exe for the context # and should match the path used for the command below.
    # The ,0 selects the main icon. [HKEY_CLASSES_ROOT\*\shell\openwemacs\command]
    @="C:\\Program Files\\Emacs\\bin\\runemacs.exe \"%1\""
    # The above has to point to where you install Emacs  
    ```

2. <span>Create a batch file called runclientw.bat and compile to exe and associate file types as needed. See [here](http://robert-adesam.blogspot.ca/2011/01/emacsclient-setup-on-windows-7-starter.html)</span>
