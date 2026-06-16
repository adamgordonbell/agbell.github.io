---
title: "Programming Throwdown"
author: "Adam Bell"
date: 2019-04-28
tags: [interview]
---

I was interviewed for the [programming throwdown podcast](https://www.programmingthrowdown.com/episodes/episode-91-functional-programming-with/).

Below is a machine generated transcription.

<!--more-->

🎙️ Programming Throwdown — Episode 91: Functional Programming (Part Two)

🗣️ Host: Jason

🗣️ Guest: Adam Gordon Bell – Engineering Manager and Podcaster

Jason:
Welcome back, everyone! We got a lot of great feedback on our recent interview with Jonas Bonér, and many of you wanted a deeper dive on functional programming. I’m excited to bring on Adam Bell, who’s been a software engineer for about 15 years and has worked extensively with functional programming.

Thanks for joining us, Adam!

Adam:
Glad to be here!

Jason:
Let's start from the beginning: What is functional programming?

Adam:
At its simplest, it’s building programs using only pure functions. These are like math functions — they take input and return output but do nothing else. This means:
- No modifying global state
- No changing data in place
- No throwing exceptions
- No reading from or writing to the outside world (e.g., IO)

This helps us write very predictable and testable code.

Jason:
Right, but that seems tough, especially since most programs do rely on some state or IO — files, databases, inputs. How do functional programmers reconcile that?

Adam:
Great question. Think of it as a design constraint. One common pattern is having a pure functional core and an imperative shell. The IO happens at the edges. You can write pure functions that process file lines, while the file reading itself is handled at the edge. So you isolate side effects while keeping the bulk of computation pure — which makes it far more testable and easier to reason about.

Jason:
Yeah, that makes a lot of sense. I remember when I transitioned from academia to industry, I realized the importance of testing. Without modular code, or if your code has hidden dependencies and globals, testing becomes impossible. Functional programming naturally enforces good modular practices.

Adam:
Exactly. If your function needs a global, you’ll be forced to refactor it during testing. Suddenly you're learning FP principles just because you're trying to write good tests!

Jason:
Right, and many folks say, "good code is testable code," but they don’t offer a guide on how to get there. Functional programming offers one.

Adam:
True. You can have "tested" code that’s still poor quality if you're mocking everything. But writing code as pure functions pushes you toward better architecture.

Jason:
So what languages do you mostly use?

Adam:
Scala is my primary language — it's a multi-paradigm language that supports both object-oriented and functional styles. I’ve also spent time learning Haskell, which is a pure functional language. We used Haskell a lot in a previous job, but because the rest of the company didn't know Haskell, we had to rewrite the project in Python. That’s when I appreciated Scala’s ability to interoperate with Java and its more gradual learning curve.

Jason:
So Scala lets you build libraries usable from Java, right?

Adam:
Exactly. That accessibility makes it easier to adopt. With Haskell, there are fewer escape hatches — it's much stricter. That’s challenging but also very powerful.

Jason:
What stack or frameworks do you use with Scala?

Adam:
We’ve used the Play Framework in some legacy projects, but now we mostly use http4s — a purely functional web library for Scala. It enforces strong FP principles: you take a request as a data structure and return a response data structure. All the behaviors are pure functions.

Jason:
What about cookies or headers?

Adam:
Those are part of the request object. You send everything in data in/data out style — so it still fits the functional model.

Jason:
Sounds much cleaner than older frameworks. I remember how confusing things could get in ASP.NET because of their hidden page lifecycle. It wasn’t obvious when things like headers were actually being sent.

Adam:
Yeah, functional frameworks avoid that confusion. There’s no secret lifecycle, just input/output.

Jason:
Some argue you can do FP in any language. To some degree that’s true, but it’s not pretty. You can force it in Java by treating classes with a single method as functions, but it’s clunky.

Adam:
Exactly. Some languages make the functional path easier. They reduce friction. If you want the benefits of FP — testability, modularity, parallelism — having a language that guides you helps a lot.

Jason:
Speaking of parallelism — FP shines here because of immutability. No shared state means less risk with threading.

Adam:
Yep. Spark is a great example — you can distribute transformations over clusters easily because the data isn't mutated. You apply transformations and return new values.

Jason:
What about inherently stateful things like databases?

Adam:
Languages like Haskell use IO wrappers — values that represent computations. Scala has something similar via Cats.IO. Instead of returning a raw value, you return IO[Int] or similar. These computations only execute when you tell them to. This approach keeps the core logic pure and makes it easy to compose asynchronous operations.

Jason:
So that’s like futures or promises, but ones that aren’t started yet.

Adam:
Exactly. You build up a chain, and only at the “end of the world” (so to speak) do you run them.

Jason:
You also mentioned something earlier — FP pairs naturally with testability. That’s a big reason people get drawn to it.

Adam:
Yeah, and also observability. You can reason about behavior much more easily.

Jason:
Let’s talk about types. FP got its start with untyped languages like Lisp, but newer languages like Scala and Haskell have strong type systems. What’s your take?

Adam:
I'm team types. Strong typing lets you express invariants directly in code. For example, returning an Option type instead of null. Now you can’t forget to handle missing values — the compiler makes sure you do. That saves tons of debugging time down the road.

Jason:
I agree. Especially when combined with algebraic data types (ADTs) and sealed traits. The compiler checks that you’ve handled all cases. It’s like trying to pattern match and forgetting a case — it’s a compile error.

Adam:
Right. That’s a big advantage! You can even encode domain logic and state machines in the type system. As the saying goes, “make illegal states unrepresentable.”

Jason:
So true. And those ideas are making their way into other languages like Kotlin, Swift, and even C++17 with optional types. It’s progress.

Adam:
There’s a conveyor belt of functional ideas feeding back into mainstream languages — Lambdas, generics, async/await, ADTs. That’s a great thing.

Jason:
Let’s touch on lazy evaluation too — that’s a defining feature in Haskell, right?

Adam:
Yes! In Haskell, expressions are only evaluated when needed. Scala has that as well via call-by-name, but it’s not the default. Laziness lets you defer work, avoid unnecessary computation, and potentially optimize for performance. But it's tricky and can lead to memory overheads if you're not careful. Space leaks can happen.

Jason:
That makes sense — like a tree of pending operations that never gets flushed. You have to know when to evaluate.

Adam:
Exactly. But when used properly, especially for GPU pipelines or big data, it’s a performance win — akin to batching commands.

Jason:
So how do you choose a functional language? Why Haskell vs Scala?

Adam:
Haskell is great for learning — it's pure, opinionated, and academically rich. But Scala fits better when you need interoperability or libraries. Need to talk to a SOAP service? Use a JVM language. Also, if your team doesn’t already know Haskell, Scala can be a more practical step into FP.

Jason:
Thanks for all of this, Adam!

🔗 OSCON Promo Segment (Around 1:03:00)

Jason and Joe promote the O'Reilly OSCON conference — discussing speakers, networking, learning tools, and opportunities to meet tech professionals from various disciplines. Discount info: Use code PT25 or go to oscon.com/PT for registration savings.

—

🎙️ About Adam’s Podcast: CoRecursive

Adam:
I run a podcast called CoRecursive. It’s an interview show where I chat with software experts on topics like functional programming, building compilers, Rust, DevOps, etc. Each episode dives deep into one topic — with curiosity and a beginner’s mindset to ask the questions others might be afraid to.

💻 Website: https://www.corecursive.com

🐦 Twitter: @corecursive or @adamgordonbell  
📧 Email: adam@corecursive.com

—

Final Thoughts

Jason:
Thanks again Adam for joining us! This deep dive on functional programming was helpful and timely. If you still have questions, shoot them to us or to Adam directly. And definitely check out his podcast.

Adam:
Thanks — this was super fun!

🎵 Intro music: “Axo” by Binarpilot  
📜 License: Creative Commons Attribution-Share-Alike 2.0