---
name: Adam Gordon Bell Webiste
description: hugo site content
---

---
./hugo/hugo.yaml
---
baseURL: 'https://agbell.github.io/'
languageCode: en-us
title: Cascade of Insights
theme: cascadeofinsights
paginate: 10
enableRobotsTXT: true

params:
  author: Adam Gordon Bell
  description: Thinking Out Loud
  disqusShortname: cascade-of-insights
  social:
    - name: GitHub
      url: 'https://github.com/agbell'
    - name: Twitter
      url: 'https://twitter.com/adamgordonbell'
    - name: LinkedIn
      url: 'https://www.linkedin.com/in/adamgordonbell/'

---
./hugo/layouts/page/single.html
---
{{ define "main" }}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            {{ partial "page-title.html" . }}
            <article class="post">
                {{ .Content }}
            </article>
        </div>
    </div>
</div>
{{ end }}

---
./hugo/layouts/_default/baseof.html
---
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
<head>
    {{ partial "head.html" . }}
    {{ partial "head-css.html" . }}
</head>
<body>
    {{ partial "nav.html" . }}
    
    <main>
        {{ block "main" . }}{{ end }}
    </main>
    
    {{ partial "footer.html" . }}
</body>
</html>

---
./hugo/layouts/_default/single.html
---
{{ define "main" }}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            {{ partial "post-title.html" . }}
            <article class="post">
                {{ .Content }}
            </article>
            {{ partial "disqus.html" . }}
        </div>
    </div>
</div>
{{ end }}

---
./hugo/content/blog/2010-10-06-project-euler-5.md
---
title: "Project Euler Problem 5 in Clojure"
date: 2010-10-06
categories: [clojure, math]
tags: [project-euler, clojure, algorithms]
---

Problem 5 asks us to find the smallest number divisible by all numbers from 1 to 20. This problem requires us to find the least common multiple (LCM) of the numbers 1 through 20.

This should be fairly easy. The algorithm is:
1. Find the LCM of the first two numbers
2. Find the LCM of that result and the next number
3. Repeat until you've gone through all numbers

First let's define a function to find the greatest common divisor (GCD) of two numbers, which we'll need to calculate the LCM:

```clojure
(defn gcd [a b]
  (if (zero? b)
    a
    (recur b (mod a b))))
```

Now we can define the LCM function:

```clojure
(defn lcm [a b]
  (/ (* a b) (gcd a b)))
```

And finally, we can solve the problem by applying the LCM function across all numbers from 1 to 20:

```clojure
(defn euler-5 []
  (reduce lcm (range 1 21)))

(println (euler-5))
```

Running this gives us the answer 232792560.