---
title: "The Accidental Engineer Interview"
author: "Adam Bell"
date: 2019-06-09
tags: [media]
---

I was interviewed on [The Accidental Engineer](https://theaccidentalengineer.com/docker-telecommute-podcasting-adam-gordon-bell-corecursive/) Podcast. Here is a machine generated transcript.

<!--more-->

Max:  
Welcome all. Max of The Accidental Engineer here. Today, we have the pleasure of being joined by Adam Gordon-Bell. Welcome, Adam.

Adam:  
Thank you. I'm glad to be here.

Max:  
For our audience that don't know, Adam hosts a similar podcast called Co-Recursive. For our audience that may not have heard it yet—and for those who have—maybe, Adam, can you give your own synopsis of the subject matter that you cover in Co-Recursive?

Adam:  
Yeah, so Co-Recursive is a software development podcast where I do an interview on each episode, usually focused on a piece of technology or a topic. I get an expert to explain to me how it works, and we're not afraid to get into the weeds of the specifics. It’s great for me to be able to learn from these experts, and I hope that the people who listen get to learn along with me.

Max:  
And in Adam's day job, Adam is a team lead of several products at Tenable, the international software security company. For our audience that are curious about the kinds of subject matter that you deal with in your day-to-day role, what types of technologies are you using on the job?

Adam:  
Yeah, so I work on application security, which is about securing applications—as opposed to network security, which is more like firewalls and such. The product I work on the most is container security. We scan Docker images. We analyze them statically, looking for software vulnerabilities, so that we can inform developers—for example, “Hey, this new library you upgraded to in Python actually has a network-facing vulnerability. Maybe you don't want to ship that.”

Max:  
This is super contemporaneous. What was the news event that happened a couple weeks ago that illuminated for the world just how insecure public Docker images are?

Adam:  
Yeah, there was Alpine. I'm not sure if this is exactly what you're thinking of, but there is an Alpine Linux distribution that's commonly used for containers because it's very small and stripped down. There was a vulnerability where you could use a null password to run as root, and it affected a wide range of versions.

When this news came out, we had to quickly add a check for it. It lit up the board for a lot of customers—we had to let them know, “You need to fix this.”

Max:  
Yeah, Docker adoption has been huge. I mean, in my previous few roles, I’ve witnessed the turning point in its popularity and adoption. The way I’ve seen it adopted often starts in development, then testing, then staging environments, and finally gets rolled out in production. Security is certainly top of mind in this flow, but running Docker on your laptop is a really popular use case. What’s your take on using Docker for local development?

Adam:  
Yeah, it depends exactly what you're doing. My team has tried various approaches. You're right that Docker became popular from the bottom up: if you wanted to try a piece of software or a new database, they'd often have a Docker image. You could pull it down and start playing around with it—and I think that's a great use of Docker.

Where it gets more challenging is if you're developing an application and want to develop it inside a Docker container on your local environment. The development cycle depends. If you're on a Linux computer, the overhead of Docker is small. But I'm on a MacBook Pro—and most of my team is as well—and same goes for Windows. Docker runs inside an invisible VM.

If you're trying to do things like hot code reloading or incremental compiling, every time you save it needs to sync over to the Docker image where all your dependencies live. That can be painful. We’ve tried that various ways, and my take is that Docker isn't quite there yet for developing inside of a container if you're not in a Linux environment.

Max:  
To step back for a moment for audience members who might be wondering why you’d even need Docker on your MacBook—which already runs a Linux-like OS—it’s really for minimizing the delta between dev and production environments. The more similar the two are, the more realistic your development will be—and the more likely you’ll catch problems before they occur in production.

Or if something bad happens in production, you can reproduce the problem more accurately on your laptop.

Predating Docker, though, you mentioned VMs. For folks who haven’t used a VM—or at least not knowingly—what is it, and how is it different from Docker?

Adam:  
Yeah, so a VM is a virtual machine. A VM runs an entire operating system stack in software. There is hardware support to make that faster, but it’s still pretty heavyweight.

In the past, to match the production environment, I’ve had to run a Linux VM on my MacBook. Now, Docker improves on this by sharing the kernel rather than spinning up an entirely separate operating system instance.

Docker was originally designed for Linux. So to run Docker on a MacBook (or Windows), Docker actually runs a VM behind the scenes. When you start up multiple containers, they all share that kernel, which is better than running five separate full VMs—but it still has overhead.

If your host OS is Linux, the overhead is basically negligible.

Max:  
So yeah, when you install Docker for Mac or Windows, it’s really Docker on top of Linux on top of Mac or Windows—it’s not Docker running natively on those platforms.

Before the existence of Docker for Mac or Windows, people used to very explicitly boot up and configure VMs manually to run Docker inside of them. It was a mess.

Thanks to Docker being a well-financed startup, we’ve come a long way. Docker's taking the world by storm in production where that business use case is really compelling. But like we said earlier, reproducing what's happening in production when you're on different environments is a problem that Docker helps with.

Adam:  
Yeah, and the metaphor of Docker “containers” is nice. It comes from shipping containers—standardized packaging for moving things around. That analogy applies well to application containers: your software and dependencies are neatly packaged and immutable. If it runs in that container locally, it’ll run the same in production.

Max:  
For sure. I want to highlight something else: you work remotely from Canada as a full-time employee of a U.S. business. One topic I’d love to cover is how you handle full-time remoteness, especially as a manager of full-time remote employees.

What's that like, and what are some of the tactics you use—for both recruiting and managing?

Adam:  
Yeah, good question. I’ve been remote at a couple of companies. I live in a smaller place. My background is, I had a previous boss I liked who switched jobs and wanted me to come work with him, but I didn’t want to move. He said, “Let’s try remote.”

Working from home, I just remember thinking a week in: this is great, I don't think I’ll go back to an office. Now, that’s me—it depends on your personality. But I really enjoy the autonomy. There are trade-offs, it may not be for everyone, but I think remote work is great.

Max:  
Fair. So when it comes to communication—when you're working remotely, how do you maintain optimal collaboration with your coworkers or teams that report to you?

Adam:  
Slack is the big one—or your chat app of choice. But the cultural aspect is probably more important. I used to be the only remote guy on a team—that can be isolating. Now I work on a distributed team with people in various places. We all embrace asynchronous communication, and it works.

But if you're the only remote one, that’s harder. You need buy-in from the whole team.

Max:  
So let’s say you're evaluating job offers—one from a partially distributed company and one from a fully remote one. Do you think it’s important to prioritize one over the other?

Adam:  
Yeah, I mean, no one is bringing me posh catered lunches here at home—so there’s a consideration, right?

I was talking to someone who was having ribs at work, while I was eating a microwave burrito.

Still, I think people should try working on a distributed team. You may find it’s not for you, but there’s value in the forced communication clarity. I wouldn't say remote is better or worse than in-person—it’s just different, with different trade-offs.

Max:  
Agreed. One of the interesting things I’ve noticed about working remotely is that all your communication has an audit trail. You can scroll Slack, Git, your email—there’s often a better paper trail than you have in face-to-face conversations. 

What’s crisis management like in a remote setting?

Adam:  
Yeah, so our team manages apps that are part of a larger microservice architecture. We use PagerDuty and respond to incidents together. We use a tool called Blameless that integrates with Slack. When someone declares an incident, they become the incident commander and pull in folks as needed.  

It creates this camaraderie—even if a metric just goes haywire but isn’t actually tied to customer issues. There’s this sense of, “We’re all in this together. Let’s jump in and figure it out.”

Max:  
Makes sense. Do you feel like fully distributed teams are better equipped for incident response due to the culture and tooling around documenting everything?

Adam:  
Yeah, I think so. You get in the habit of clear logging and communication. Even if the issue turns out to be minor, everyone's ready to pitch in. That shared experience builds connection.

Max:  
Do you have any parting advice for people starting their first remote job?

Adam:  
Yes—try to meet with your team in-person a few times a year if you can, even for planning. It’s less about work and more about building relationships.

There are also tools like CoffeeTime, which randomly pairs coworkers for virtual coffee chats. We use that, and it’s a nice way to connect.

Honestly, even in office environments, people sometimes just wear noise-canceling headphones and Slack all day. A lot of the same principles apply whether you’re remote or not.

Max:  
That's true. We'll include links to some of these tools—CoffeeTime, Blameless, etc.—in the show notes.

For teams that rely on Google Hangouts or Zoom, it really helps maintain interaction.

Do you have any exciting technologies or programming languages you’d like to plug before we wrap?

Adam:  
Sure. My team works in Scala—a functional programming-leaning JVM language. My podcast also covers languages like Rust and Haskell. I lean towards functional programming and using types to build better software.

Even using TypeScript over JavaScript is a step in that direction—it’s worth exploring.

Max:  
We'll throw links in the show notes for Scala, Rust, etc. Honestly, I've never written a line of Rust and need to check it out myself.

Adam:  
It's super interesting, yeah.

Max:  
I encourage our audience to go check out Co-Recursive, Adam’s podcast. Adam, thank you for coming on.

Adam:  
Thank you very much. It was great.

Max:  
For more, visit us on iTunes or our website at theaccidentalengineer.com.
