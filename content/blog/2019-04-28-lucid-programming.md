---
title: "Lucid Programming Interview"
author: "Adam Bell"
date: 2019-04-28
tags: [media]
---

I was interviewed for the Lucid Programming Podcast.

Below is a machine generated transcription.

{{< youtube C0PuCgQrxZU >}}

<!--more-->

## Introduction [0:01 - 0:42]

[0:01] **Vinnie**: Welcome to the Lucid Programming podcast, a podcast where we talk to fellow software developers, engineers, YouTubers, entrepreneurs, and all-around interesting people. If you want to listen and gain perspective and how to improve your skills, become a more effective software developer, I hope that these conversations serve to enrich your learning experience and deepen your appreciation for various topics.

[0:25] **Vinnie**: If you like content like this and wish to support it, there's a PayPal link in the description of this video. All proceeds go to improving the content on this channel. Alternatively, subscribing and liking and sharing and commenting do a great service to support this channel and also helps to encourage other developers like yourself improve in their own domains. Thank you for all of your support and encouragement.

## Who is Adam [0:42 - 1:21]

[0:48] **Vinnie**: Alright so welcome to the third episode of the Lucid Programming podcast as it has been so named. The guest today is Adam Gordon Bell. He is, as he says on his website, developer podcast Vinnie and a human. He's a software engineer and he likes to build software and he's based in Peterborough, Canada. He works remotely with developers all across the world and he is also the Vinnie of the CoRecursive podcast.

[1:14] **Vinnie**: In addition to that, Adam also writes a blog, and the links for both the podcast and the blog are going to be available in the show notes where I'll link to his website if you want more information on Adam.

[1:21] **Vinnie**: The focus of this podcast is a bit impromptu. Adam sounds like a really interesting guy that reached out to me a couple weeks back. We both had a lot of overlap of interests and we're just gonna kind of see where this conversation takes us.

[1:34] **Vinnie**: One of the things Adam brought up was the focus of the technique of bullet journaling and the application of that technique to being a better software developer. So that might be a reasonable place to start, but first before we do that, Adam, if there's anything that I kind of missed, is there anything that you want to, you know, mention about yourself? Feel free to, floor's yours.

## Where to Find Adam [1:46 - 2:37]

[2:00] **Adam**: The podcast is just a great medium to talk to people. I'm sure that you find the same thing. So I mean I would definitely recommend people check me out there or on Twitter.

[2:06] **Adam**: Well yeah, the blog exists, it's just, you know, life gets in the way of a lot of blogging sometimes.

[2:12] **Vinnie**: I know sir. That also, that's as a vlog as well, and I feel I don't think I've updated the thing probably for about a year so you're in good company.

[2:25] **Vinnie**: Yeah, well. So is there anything about the... I know you have the CoRecursive podcast, is that something that you frequently update? Is that anything that you know, maybe the audience here might find of interest? CoRecursive sounds programming-esque, so I think that there might be some overlap and I think the audience could benefit from hearing what you do.

## Adam's Podcast [2:37 - 3:20]

[2:49] **Adam**: What I do is, I, you know, I really like to learn things. I'm very curious individual. I've been, you know, developing software for a long time, but there's a seemingly unending number of things to learn.

[2:55] **Adam**: So my podcast is basically an interview format where I would bring on an expert about a topic and, you know, kind of try to learn about it from them.

[3:08] **Adam**: A lot of the shows have had a focus on functional programming because that's an area I've been very interested in, but it kind of, kind of goes all over the place. And yeah, I totally recommend it, it's awesome.

[3:20] **Vinnie**: Definitely. And, and you mentioned functional programming, and I guess my background is more, I sort of cut my teeth in the procedural world of programming.

[3:31] **Vinnie**: And functional programming as someone else who also, I guess, gets bit by the learning bug and gets very intrigued by learning new cool tricks and techniques, it's kind of a tempting thing to jump into the world of all of these different languages and all of these different paradigms of programming.

[3:49] **Vinnie**: I guess when you are also, you also have mentioned that you're kind of an avid learner, how do you find balance between, I guess, jumping into something new? I don't know if it's new for you, anyway, it's new for me, functional programming, or maybe a new language.

[4:01] **Vinnie**: You have to kind of, a trade-off for what you kind of figure out is like the optimal calculus for learning something and then applying it. Or do you just kind of dive in? What's your process for, for learning a new technique or, or, you know, language when you kind of stumble upon it?

## Learning New Techniques [4:15 - 5:30]

[4:26] **Adam**: And I think that, you know, functional programming is kind of a deep concept. So I try to think about things like, there is a difference between like, like surface level concepts and deep things.

[4:39] **Adam**: So I could spend a lot of time learning about, you know, new changes to, to a library that I did, I use quite frequently that's coming up, but that knowledge probably, you know, will will quickly age.

[4:52] **Adam**: Whereas if I look into more of a deep topic, so it could be functional programming, it could be machine learning, it could be data structures, which I see you do some videos on, hmm, that kind of deep knowledge is not gonna age out as much.

[5:03] **Adam**: So you can spend time learning about function programming or data structures and assuming you're gonna do this software thing for a career, like it's never gonna be a bad investment.

[5:16] **Adam**: Whereas if you learn about, you know, the newest member library or, you know, the newest React style, I think that it won't be nearly as valuable five years from now.

[5:30] **Vinnie**: I totally agree. And I, I don't know if you sort of went to school or had any classes in computer science, but I can tell you from at least from my perspective firsthand, probably about 70 to 80 percent of the, especially the programming-based classes that I had, which were very language-centric ones that really focused on specific, maybe technology or language, really just very fastly got outdated.

[5:57] **Vinnie**: And, you know, the algorithms, data structures, the things that are probably not going to change anytime soon, those are really just kind of the mainstays, the, you know, the bread and butter of the computer science world.

[6:08] **Vinnie**: And I mean, anything that I can conceivably imagine in the future is probably going to be based on some, one of a thorough understanding of those topics. And that, that's kind of the stuff that I value.

[6:20] **Vinnie**: You know, I try to kind of convey some of the stuff. Of course, you can't get away with the languages that are hot at the time, the things that are kind of, you know, used as the, let's say, syntactic sugar of the programming world to convey those concepts. But definitely, yeah, focusing on the things that are going to have the biggest staying power, I think is really, really kind of crucial.

[6:40] **Vinnie**: So I guess, I, maybe this leads into another question, which is: as you were kind of a full-time developer, how do you balance the work that you do which presumably relies on skills you've already developed and, you know, let's say diving into a new topic? Do you make specific time to, you know, explore new concepts, new languages, do you try to incorporate that in your work? How does someone kind of stay relevant in a field that really requires relevancy when you're kind of doing this full-time?

[7:08] **Vinnie**: I find like stagnation is a big problem. Do you have any, do you have any tips or tricks that you use to kind of stay relevant for yourself like I... 

## Just-in-Time Learning [7:14 - 8:20]

[7:20] **Adam**: I will tend to focus on just-in-time learning. So for like, because I said before like, whatever, don't learn this latest and greatest thing, but obviously you do need to learn these things as you complete your job.

[7:31] **Adam**: So what I, you know, do is kind of, when I need to know something on the spot, like that's a great place for me to learn like that specific thing, right?

[7:43] **Adam**: So maybe like, I want to learn about, like maybe I have to solve some very small machine learning problem, and I can just look up like how to call the right things into whatever library I'm using. But maybe that will, that will spark in me a curiosity to do with this concept in general.

[7:57] **Adam**: So, so I think you can separate these two things, right? For my day-to-day job, I need to know these specifics that may age quickly, but maybe I'll develop an interest in some deeper aspect of it.

[8:09] **Adam**: And for that, you know, I can go deep on that, like, you know, as you know, something I do on the weekend, maybe not even with, not even with an eye towards using it in my day-to-day job, but just kind of developing some deep knowledge in an area. And usually I just, I just let that be driven by my interests.

[8:32] **Adam**: So I think they, you know, it can, like, I like to build things with software. Sometimes day-to-day jobs are very, you know, McKim mechanical or you don't get to get deep into the details of something. So, so take that time later on, find an exciting project whether it's, you know, weird graphics or machine learning or functional programming, and just do it for your free, for recreation, for fun.

[8:54] **Vinnie**: I think that's a very good example. I think that especially if you got into programming kind of full-time as a profession, you probably, I mean, one probably has sort of independent interest that is irrespective of the job they're working at in that subject.

[9:07] **Vinnie**: So I'm always the case, obviously, you have a lot of people that kind of get into it for just treating it purely as a job. But I think the concept of just-in-time learning that you mentioned is a really important one.

[9:20] **Vinnie**: And I find this to be a bit of a struggle for me, mostly because oftentimes I'm a bit of a, what should I say, I read a lot of books at the same time. And I think that a lot of the information that I obtain at any given time is probably not immediately used, and therefore it's probably just, it's going to atrophy over time.

[9:39] **Vinnie**: And I've really tried to incorporate that just-in-time learning. I really like that phrase because it kind of reminds me of, you know, sort of like a programming term already. So I like, I've really been trying to actively incorporate that type of philosophy into things that I do. If I learn something, I try to immediately apply it. It's kind of like when you, when you meet someone for the first time, saying their name after, to kind of like reinforce that, that concept in your brain.

[10:07] **Vinnie**: And it's, it's something that I struggle with because, you know, I assume like yourself, you're really like learning. And it can be really productive procrastination is one of those things that I've, I guess, in that front, I've kind of struggled with.

[10:19] **Vinnie**: And maybe this, this might be kind of a, a segue to a concept that you brought up before that I thought was kind of interesting, especially in the domain of software development. And that is bullet journaling. And I, maybe if you could kind of briefly explain the concept in general and then, and then maybe give a little bit of context to how you use this to be a better software developer. Would that be okay?

## Bullet Journaling [10:31 - 12:42]

[10:48] **Adam**: Bullet journaling is a technique for taking notes and there is a book and I actually have it here with me: The Bullet Journal Method, Track the Past, Order the Present, Design the Future. So I mean, that makes a lot of promises there.

[11:01] **Adam**: The actual technique, this is fairly simple and you probably don't need a book for it. So, the thing I like is, if you have a system of taking notes that you can count on, that you kind of use in a, in a repeated way, and it's always available, that allows you to kind of take some of that burden off yourself of like keeping track of, of various things.

[11:26] **Adam**: So the system, the bullet journal system I use is, I have a, have a book of blank pages, it's, it's sitting next to me, the pages are numbered. And then each day I will write at the top of a page or sometimes midway down the page, but I'll write today's date and underline it. And then as I'm going throughout my day, like I always have this next to me at my computer.

[11:49] **Adam**: And the bullet journal has, they have a system that they call rapid logging, which is just a way to take point form notes and kind of categorize them very quickly. So let me describe some of those.

[12:02] **Adam**: They just use a number of symbols. There's one which is just a dot for, it to do, there's one which is like a circle, which is for like an observation, and a dash is just like a note. And so as things come up in the day, for instance, somebody reaches out to me on my team and says, okay, I noticed this thing that you developed had this problem, somebody's complaining about it and I fixed it.

[12:30] **Adam**: And so I might just quickly take a note for myself and I will use the circle that's kind of for an observation, sit like, "Tom, Tom went above and beyond, fix my thing." Like I might just say, "Tom fix X," kind of write that down.

[12:43] **Adam**: And so if something else comes up like, somebody wants me to look into X, so just put a dot and write that down. And so over the course of the day, you know, I have a running list of my to-dos and my observations.

[12:54] **Adam**: And it's a very, so from like a data structure type of perspective, it's kind of a, a quick write system. So it's very easy to write down whatever your thoughts are because you just write them under today's date.

[13:09] **Adam**: And then the, the problem with that, I guess, is like, retrieval, what's that...

[13:20] **Vinnie**: Retrieval, the, the read process is, is a bit, is a bit inefficient, right?

[13:28] **Adam**: Yeah, yeah, exactly. So if I want to see all my observations, you know, for the past month, then retrieval is hard, as you're saying, because, you know, they're scattered across all the days.

[13:38] **Adam**: So the bullet journal, I don't think this is how they would describe the process, but they, I'm a software guy, so this is my way of thinking about it. So they have a batch process step.

[13:45] **Adam**: So at some cadence, I think they recommend like at the beginning or end of every day, you would go through what happened in your previous day and kind of categorize that. So, you know, at the end of the day, I might look at whatever to-dos are left, see if they're still valid, and kind of move them on to the next day.

[14:04] **Adam**: And then I may take my observations and put them somewhere. So what I do is like, we have a, we have a sprint system at work. So every two weeks, you know, we, our work is broken up into two big chunks. And in the end, we have like a retrospective where we talk about what went well and what didn't.

[14:23] **Adam**: And so I have a section in my book for these retrospective notes. So my observation about Tom would get moved over to there. And then when it's time for the retrospective, I mean, everybody thinks that I spend a lot of time thinking about how great everybody was because I have a lot of observations, but really it's just an aspect of being able to quickly jot these things down and then batch process them into a list.

## Why Write in a Text File [14:42 - 16:01]

[14:50] **Vinnie**: It's really interesting. So I know you mentioned earlier like, you know, kind of understanding this process in your words in terms of a software guy, which I think there's a big open world for book series based on understanding, you know, X in terms of the software guy, cooking is, I mean, I think there's a lot of, there's a lot of open area there, cooking for engineers. Oh man, there's, there's an Amazon market for that, I'll tell you.

[15:10] **Vinnie**: So like that might be that, that might, if anyone's listening and they're looking for a niche, that, that could be it. But you say something kind of interesting to where, well, I guess one thing that I kind of noticed, that as a software guy, you mentioned you have a physical, you know, dead tree paper copy journal that you use for this process. And I suppose, like, a lot of the people that I would work with, as well being a software guy as well, a lot of people would probably use some in electronic medium.

[15:46] **Vinnie**: Is there anything that you particularly like? I mean, one of the things I think, whether or not it's an electronic medium or dead tree copy, the right process is fast. Is there anything that specifically makes the pen to paper aspect of this more attractive or easier for you? Or I guess, why do you prefer that? Being, being someone who is very well versed in something that, you know, you could probably use an electronic supplement, what is the, what is the reason there?

[16:12] **Adam**: Yeah, so I do actually also have a different need, but so that's a good question. Why not write them down in a text file or something?

[16:26] **Adam**: So I like the fact that my, my bullet journal here is, it's always at hand. So I haven't sitting here with a pen right now, I'm just a list of to-dos.

[16:32] **Adam**: There's also some information like, some studies that have been done based on students. University students nowadays tend to all have laptops and it kind of, write out notes as the teacher speaks. And they've done some studies in, to and found that they, the people who actually do written notes have much less detailed notes but do a lot better in class.

[16:59] **Adam**: And the hypothesis is that, like, writing things out is slower, like physically writing it on paper. And because of that, people have to kind of compress what they're saying, you know? You might just write down like two or three words for a point rather than, you know, verbatim sentences.

[17:18] **Adam**: And that, that act of like compressing your thought into just a couple words, so it's actually like a process of thinking that's actually processing your thoughts, right, to get them into a condensed form and then understanding that form. So it's, and there could be, you know, they theorized something to do with just the physical process of like moving your hand, you know? I don't know, the brain's strange, who knows how it works.

[17:43] **Adam**: Yeah, I just like that it's always at hand. I think that's probably a benefit.

[17:48] **Vinnie**: And the, yeah, the act of writing I find to be particularly, and this is probably something that, maybe not evolutionarily because I don't think we've been writing for quite that long. But there's kind of this, this tablet mentality where writing something down, I've noticed this personally too, it does help it to stick better, better.

[18:07] **Vinnie**: And it's just not something that you can particularly replicate one year when you're writing or typing, I should say, in any kind of electronic medium.

[18:13] **Vinnie**: I've seen some people that are just absolutely ninjas at, you know, being in the curriculum and computer science earlier on and just seeing people that just made some beautiful notes in real time, like in a LaTeX or something like that. It was really just, it was something to marvel at.

[18:32] **Vinnie**: But I, yeah, I don't know if they really, they, they made some beautiful notes. I'll mention that. But I don't know if they really did any better when it came to, let's say, test time or application time. So I think there is definitely something there for kind of writing it down, pen and paper, you know, sort of optimizing for a low-tech solution. So, yeah, good, feel free to elaborate on that.

[18:48] **Adam**: Yeah...

## Learning Better by Hand [18:50 - 19:56]

[19:05] **Adam**: Yeah, amen. Yeah, that's right. I mean, I think that their focus becomes more on getting the pristine notes than actually, you know, like filtering this information through themselves and kind of learning.

[19:18] **Vinnie**: That's exactly right. And I think I've also fallen victim to this where, again, it's another form of productive procrastination where I will try to like render... This, this happens even when I'm writing things down on pen and paper where I will write something down and my handwriting is akin to a blind third grader who doesn't have hands. So it's bad, but anyway...

[19:43] **Vinnie**: Like that, I try to really take effort when I'm writing something down to make it look good. And I feel oftentimes my effort is misguided in the sense that I'm spending too much of my auxiliary power in making it look good and not enough in doing what you previously suggested, where you're kind of taking that information content that you get in real time, condensing it, condensing it down into some collection of smaller words, you know?

[20:08] **Vinnie**: You're doing some sort of compression algorithm on it in real time and putting that down in your notebook. I feel like that, that is something that I personally need to work on. But I think that, yeah, between the two mediums, at least for me, writing things down, despite the fact that I might not, my read process is really inefficient because my writing is terrible. But, you know, aside from that, I definitely do think there's something there.

## Bullet Journaling in Tech [20:32 - 21:12]

[20:32] **Vinnie**: I also wanted to ask a little bit about this technique. And you mentioned when you did, you know, some of these like touching points with your team, you know, you sort of very seemingly very quickly replicated some of the things like, "Oh, you know, Tom did a great job."

[20:45] **Vinnie**: And how was this person able to replicate that so quickly? Have you, have you elaborated on your process to your teammates? And, and is this bullet journaling something that you have seen applied to tech? Or is this something that you have just taken and kind of made your own system?

[21:04] **Adam**: But I think that it's a very personal thing, right? So I don't think it's something that could be mandated at a, at a team level, right? Like everybody has, you know, their system.

[21:18] **Adam**: I feel like part of the key of my system is that it's my system and I just know, you know, if somebody asked me to do something, I write it down on the spot and I know that later I will get to that, right? So somebody else may have a different system for handling that.

[21:31] **Vinnie**: I find that to be... I did, by the way, if you had more there, I don't want to interrupt.

[21:38] **Adam**: Yeah, so if you look at, just a tangent, if you, if you look at bullet journals, like just go onto Instagram or Twitter or something, search for "bullet journal," you will just find these people who do like, like it's, it's beautiful. They take these, you know, they have like eight color markers and there they're building all this stuff themselves.

[22:04] **Adam**: And I think if you try to look up bullet journals, you'll find these people that are just with beautiful penmanship and doing all this complicated stuff. And so that's not, that's, that's not me. I have the same writing. I'm just using, you know, and I don't even think it's the point of the system. The point of the system is to have like a system for quickly jotting down things. But I think...

[22:22] **Vinnie**: In our Instagram generation, things become, alright, that's, and that's a good and a bad thing for sure. And, and part of that is so... Okay, so having good penmanship is definitely a feather in your cap when it comes to this type of system.

[22:41] **Vinnie**: If you were to... Have you seen any apps that, that take on this bullet journaling thing? Is that, is there any application that exists? And actually, I don't know too much about your software engineering background like, are you, do you develop apps on the side?

[22:52] **Vinnie**: Like I kind of wonder if maybe this is something that kind of is calling out for, you know, some sort of electronic equivalent, even though we just spent lost, you know, 20 minutes or so talking about why it might not be the case, but is there any, is there any hope for that? I mean, for me...

## Personal Wiki [23:04 - 23:38]

[23:09] **Adam**: It's a physical writing process. And but I will tell you that just to complicate this note-taking topic, I do have sort of a knowledge base of like, kind of like a personal wiki that I keep in text file format that kind of relates to this process.

[23:25] **Vinnie**: And is this wiki public at all? Is it something that is associated with the blogger? Is, again, this is just kind of personal notes for yourself?

[23:31] **Adam**: This is just personal notes for myself. So yeah, please...

## DArchive [23:38 - 27:51]

[23:47] **Adam**: So, so as I said, the bullet journal system has this kind of like rapid logging. And then they cut, you kind of go through and pull out things and move them to different sections on like, kind of a batch process.

[24:01] **Adam**: So what I do is, I have, I use this program that is called D Archive. And basically it lets you have a folder full of text files that are in down format. And it kind of makes a little bit of a wiki out of them so that you can, like, you can, if you put like hashtag data structure, then that'll become a link just in your text file note. And when you click on it, it'll find all the notes that relate to that.

[24:31] **Adam**: And if has some other features like, you know, it lets you mark things up and mark down, you know, pretty lightweight format and give them titles in the search across them. But mainly it's just a whole bunch of text files.

[24:43] **Adam**: So what I would, what I do is with my retro observation, rather than move it to a different section of my paper notebook, I just actually have a file on my computer here. So that I would just take my, my three word statement about Tom and I might expand it a little more and actually type it out into my retro section of my notes.

[25:09] **Adam**: And the benefit there, you know, maybe isn't huge compared to, compared to just putting it in my notes. But where I find it's really valuable is for learning. So you were talking before about reading a book and, you know, not knowing how much of it sticks.

[25:27] **Adam**: So, so I kind of applied this system to learning, right? So if I were reading, well, let's say, let's say I'm watching your videos and we're going through stuff about data structures and I have some sort of thoughts about, you know, how like a linked list relates to, you know, some other concept I learned somewhere else.

[25:47] **Adam**: So I might just make a little note in my little bullet journal here that says like, you know, "linked lists is like..." I, I can't, I can't argue that point, and then like, later when I'm processing my notes, hopefully that still makes sense to me and I see, yeah, I'm like, "Oh yeah, no, it really, you know, cuz you can traverse through a linked list and you can...

[26:13] **Adam**: The Reynolds says mustache. I'm not really sure. So I would take that and I just open up my text file note system and I would paragraph or so to a new file. And maybe I would give that, you know, the data structure tag. And and this, that's kind of like processing it where, like, first of all, I'm writing it in my book in point form. And then later I'm kind of expanding on it in my own words.

[26:38] **Adam**: I think that this is kind of where learning happens, like I'm making learning like a physical process where I'm actually like typing things over.

[26:43] **Vinnie**: So I think just to clarify on the other very apt analogy between linked lists and Burt Reynolds, I've sort of heard of using this time type of technique for, let's say, you know, you want to remember to pick up milk, eggs, and, you know, this is this whole laundry list of things that you need from the grocery store, right?

[27:02] **Vinnie**: And you can't possibly keep all that in RAM just to make it another analogy to the... Yeah, so that, there we go. So that's another point for me. So we're, we're neck-and-neck here. But yeah, so like, if you want to kind of like make sure that you have all of that stuff, you don't forget it without running it down, you know?

[27:21] **Vinnie**: I guess the analogy that I've heard, or the technique that I've heard, rather, is to make each of those items as ridiculous and kind of thread together in a narrative. So if you need to, you know, remember to pick up milk and eggs and bread, imagine a huge cow that lays eggs that, you know, somehow is like living the land full of bread. And that narrative structure is going to allow you to, you know, have better recall.

[27:40] **Vinnie**: So is that kind of the, is that sort of the same technique that you are sort of alluding through there with like connecting, let's just say, linked list with something that's a little bit unrelated but has some relevant concepts? Or am I missing the mark totally on that?

[27:51] **Adam**: I think that I just gave a bad example. So let me, that was, it was ludicrous, but not for any sort of memory purposes.

[28:04] **Adam**: So let me say instead, I, I'm learning about docker containers, and I realize that docker containers, the way that they store data is a lot like how git stores data. And so maybe I just write in my bullet journal, you know, "docker equals git."

[28:24] **Adam**: And then later in my note system, I might kind of expand on that, write a paragraph or two about the... And that, and then that kind of lives in my little personal knowledge base here. And that's just a way for me to kind of to better understand these things by processing it.

[28:42] **Adam**: But it also means I'm building up this knowledge base. And that thing about how git relates to docker, maybe that could be, you know, maybe that could be a talk I could give that work, maybe that could be, you know, a blog post I write, or maybe it's just a thought I have that I want to jot down.

[28:56] **Adam**: But I really like this idea where, like, your thinking process is not just sitting there, you know, holding onto your chin, but it's this like active thing.

[29:02] **Vinnie**: I, oh, I guess I want to ask, maybe to elaborate on that a little bit in the sense that you did mention that the bullet journaling process is read heavy. However, how often do you read from it? And I wonder like, maybe, is it just the fact of writing it down and the process of kind of putting it on paper that is the most valuable part of this practice?

[29:25] **Vinnie**: How often do you find yourself going back over the notes and, you know, do you find that to be valuable? Or do you find just really the act of putting it down to be more valuable?

[29:33] **Adam**: No, that's a good question. Too much, definitely like for to-do's, like when I'm just writing, you know, I write down to-do's and then like as I do them, they'll get crossed off. So, so kind of at that point, there, they're dead, right? Like once the to-do is done, doesn't have a lot of value.

## Separate Notebooks [30:00 - 31:34]

[30:00] **Adam**: But the more, the more involved things like I was talking about for my learning process, kind of expanding on things and depth, like I find that very valuable. And it could, it could lead to me, you know, like deciding to interview somebody for my podcast because, you know, I had this interesting thought and I Google bit and there's somebody there, or it could, you know, it could lead me to explore an area.

[30:23] **Adam**: So I, I don't know. So I guess it's hit or miss. It depends on the context, right? Whether an observation is gonna be something you want to, you know, learn further about or whether it's just a quick throwaway comment.

[30:35] **Vinnie**: So do you find yourself looking back on the things that you've written down frequently or do you find yourself writing the content more frequently? I guess I wonder which one of those takes up the most, the most CPU cycles.

[30:49] **Adam**: Yeah, yeah, that's a good question. I mean, I think that I don't know. So I, I didn't look through my notes, but also I think sometimes it's just helpful to get something off of your head to know that it's stored somewhere. So it can be both.

[31:11] **Vinnie**: Do you have any separation between the bullet journals that are primarily for, let's say, your job, for learning concepts, and for the things that are kind of like with respect to just to-do things that you need to do around the house or whatever it might be? Are these, are these separate notebooks or are these kind of all amalgamated together into one notebook?

[31:28] **Adam**: Yeah, I don't...

## Remote Work [31:34 - 33:16]

[31:34] **Adam**: I don't know if that's interesting. I don't know if this complicated at all but like, so I, I work remotely from my home office and so I'm assuming, and I've been doing so for so long that I don't recall what it's like to, to leave those to go to work.

[31:54] **Vinnie**: That sounds glorious.

[31:54] **Adam**: Yeah, so I imagine that, you know, if I did have a separate place that I went to that I may have a notebook in each place, you know?

[32:01] **Vinnie**: Now, I, I guess this is gonna be a bit of a segue, but I know that, I mean, for a lot of developers, you know, remote work is really attractive. And I have found in my own experience, obviously, I can only speak on my own experience, but for working remote, it's very nice. There's a lot of perks. I feel like oftentimes I get much, much more done. The day is much longer for good, for better, for worse.

[32:33] **Vinnie**: However, finding that separation is, you kind of alluded to a little bit earlier, is difficult figuring out when working hours start and end, figuring out what psychological triggers need to exist in order to have the work start and have the work end. I find myself struggling with these things.

[32:52] **Vinnie**: I kind of assumed that a lot of people listening might also, especially if they're in the development world, if they can work remote or if there are full-time remote workers, this can probably be a bit of a tough spot for them. At least I know it is for me.

[33:03] **Vinnie**: Someone who has gone through remote work and someone who doesn't even remember what it's like to go to an office, what have you found to be particularly effective in staying productive in, you know, essentially keeping balance? What element of this do you find most challenging? Is it, is it staying focused that your work isn't leaving the work behind? Where, where do you find the challenge? And again, that's a lot of material there too.

## Challenges [33:16 - 34:24]

[33:27] **Adam**: I find that both of those are challenging in their own way. So for keeping the work separate, if my home is my office, I don't exactly know when to shut off. And then on the other point, staying productive for sure, like basically if your office is your home psychologically, you know, you, you open the front door and you go home and you're just kind of home, right?

[33:54] **Adam**: You know, like I think that there's a bit of that that needs to be altered in a way where you kind of view it as both your home and your workplace. So I personally, for me, I find both of those challenging. And I know that those both have a lot there. So I don't know if there's one of the other that you kind of want to, you know, chew on or elaborate on. I mean, any, any points of insight would be very much appreciated on my end.

## Working from Home [34:24 - 35:52]

[34:24] **Adam**: I know, so an interesting thing is for me, I find that it's not so much separating work from home that is problematic. I think what's problematic for me is sometimes getting a little bit stir-crazy because I just don't go a lot of places.

[34:44] **Adam**: So I think that like, you know, working occasionally like one thing I've been doing which, which sounds so simple, but it seems to be quite useful for me is just like on Fridays, I work in a different place in my house. So I have a home office and that's kind of my work zone.

[35:04] **Adam**: And some people might tell you like, yeah, keep that work zone, you know, that's your work zone, you know, and then there, the house is here, your non-work. So but actually I found it useful because it is just a small office and I'm spending all my time here to actually, you know, to mix it up, to travel around the house, to work in the kitchen or the living room sometimes. So I found that useful.

[35:27] **Adam**: I've found Slack, so we, we use Slack of my work. I don't know if you're familiar the shirt. Just a brief explanation maybe for anyone who might not be, this is just like it's like a chat app but within your corporation. So it's like WhatsApp or IRC, but with all the people in your company.

[35:46] **Adam**: And my company is quite distributed and people in different time zones and we use Slack very heavily. I found Slack to be probably the most challenging thing for having a work/life separation.

## Lighting [35:52 - 38:47]

[35:58] **Adam**: Because just, and I don't even think that has to do with not being in the office. I think that it's true of people in the office too. We just have the Slack app on their phone and they're just always getting messages about this or that. But so that is a challenge.

[36:11] **Adam**: And going back to being stir-crazy, I know that we are both, I'm also residing in Canada as well. And part of stir craziness and cabin fever sets in when the weather gets cold. We're getting kind of a turn for better weather right now. And I feel like your work, your office kind of expands to the other, let's say a coffee shop, and you're more likely to go out at least. I know I am when the weather is nicer.

[36:37] **Adam**: But switching up different rooms in your house is definitely, I think, a good way to kind of keep things fresh. But for those of us in cold climates like you and I, do you find like you were, you know, your energy levels to be like dipping in the winter versus the summer? And if so, do you have any kind of I've heard of these like lights that can be bought that sort of I think they're called seasonal affective disorder lights.

[37:07] **Adam**: And they're basically just lights that can simulate the light of the Sun that we here in Canada lack a bit of to kind of replicate that and to sort of alleviate any, I guess, depression-like symptoms? Are there things that you can do or that you do perform in the colder darker months that help you through that time?

[37:34] **Adam**: At one point I had one of these lights in it and I did really liked it. And then I think the bulb burnt out and I never got a new one. But I found it like, I guess it does wake you up is what I found, like.

[37:47] **Adam**: I think part of the problem that people have with the winter in more northern climates is like the Sun just isn't bright enough to kind of tell you like, "Hey, it's morning, like, get going." Right? And then at the same like, it's, it's kind of the reverse of people have trouble sleeping because they stare at their phone all the time. It's just like the dreariness of the of the... The Sun isn't there.

[38:07] **Adam**: So the lights can be effective that kind of, you know, telling you like, "Hey, it's the day," and making sure you have a nice like, what is it called like a circadian rhythms? You're kidding a rhythm?

[38:14] **Vinnie**: Yeah, yeah.

[38:21] **Adam**: But I don't honestly, I don't have too many tips besides that, like exercising, which I don't do as much as I should, is kind of a miracle for a lot of, you know, lulls. But that's all I got.

[38:34] **Vinnie**: Yeah, I think that those are both pretty good. I, I guess I've never had one of those lights. I might give one of those a shot maybe the next winter that comes around here. And exercise, yep, I think that's definitely a very good way to kind of mitigate some of those, some of those seasonal disorders that arise, especially in the northern colder climates as you said.

## De-drudgery [38:47 - 43:01]

[38:52] **Vinnie**: As when it comes to, I guess, just being productive in a home office, I guess, are there any like, I know there's like Pomodoro techniques and things like that that a lot of the productivity gurus used for other domains as well, which is, you know, basically for those who don't know, is just kind of a method that you have like 25 minutes on a task uninterrupted, totally focused, and then five minutes off. And every 25-minute set is referred to as a Pomodoro.

[39:23] **Vinnie**: And have you used this with any effectiveness? If so, you know, have you found it to be useful? Do you find to use them consistently? If not, are there any other, you know, kind of techniques or things to keep you particularly focused when you're in the midst of work?

[39:43] **Adam**: Yeah, that's a great question. You know, I think that the interest, interest drives focus in, in certain ways. Eliminating distractions is certainly useful. I, I have not used this Pomodoro Technique, but I have read this book called "Deep Work" by Cal Newport. I definitely recommend it. Don't, have you heard of it?

[40:07] **Vinnie**: Yeah, I've read, I read all of Cal Newport's books. I think, I think he's a newer one, which is, beYou know, it's after "Deep Work." I've totally forgotten the name of the newer book he wrote, but yeah, "Digital Minimalism," yes. That's exactly...

[40:21] **Vinnie**: He's a computer scientist, which is kind of interesting because he's definitely in this niche that I think, you know, you were kind of also in where you're sort of taking these, you know, for lack of a better term, like productivity techniques and sort of applying them in the realm of computer science.

[40:34] **Vinnie**: But I really found "Deep Work" to be a very impactful book. I read his blog as well, which also kind of elaborates on a lot of the concepts where he's very, he's very adamant about removing like social media. He's kind of, he doesn't want any social media in his life because he views it as complete destruction with no value.

[40:56] **Vinnie**: His book covers a lot of different territory. I've not read "Digital Minimalism." Have you, have you read it?

[41:03] **Adam**: No, I haven't. But the deep work concept, right, I think it kind of relates to that Pomodoro, but I mean, he's just in a much broader way. He's just saying like, find out what the important thing is of your, of your job and then make sure that you have just like dedicated time with no distractions to work on it.

[41:22] **Vinnie**: For sure. And I think that's definitely probably the most valuable thing you can get from that. But, but you did mention, I think, you know, sort of interest drives focus. And I kind of wonder, you know, with any job, even the job that is, you know, the most interesting job in the world, the job that you love, a job that you get a lot of fulfillment from, there's going to be those components of any job that are gonna be less fulfilling and there are going to be a little bit more dry and harder to get through.

[41:48] **Vinnie**: When you go through those components of the job, and maybe this is, you know, I'm speaking from perhaps, you know, position where this is clearly a weakness of mine. And I may be perhaps selfishly asking someone who, like yourself, is probably pretty well versed and, you know, battling these sorts of dragons.

[42:06] **Vinnie**: So when you encounter these types of problems in your own work, you know, do you find any particular type of technique or process to be kind of helpful for getting over that hurdle?

[42:20] **Adam**: I mean, there's always drudgery to certain extent in your job. But I mean, I don't think that I have a solution for that like myself. I think that a strategy that I employ is, you know, avoiding the things that are, that are drudgery until they become so urgent that they must be, that they must be tackled. So I would recommend that no strategy.

[43:01] **Adam**: What, what do you struggle with? What's, where's your problems lie?

## Learning [43:01 - 46:10]

[43:01] **Vinnie**: Well, I mean, I guess just on that point, if I am working through a particularly unpleasant part of a process that overall I feel is fulfilling, getting through that one little segment to get to the next point, I find to be sometimes a boulder that is larger than it should be.

[43:21] **Vinnie**: And so my biggest problem there is being unable to approach that or just delaying and procrastination. So procrastination is probably a big part of that delaying process. And I guess as, as sort of a dumb mammalian creature that I am, I need to fear a way to kind of manipulate my own psychology to not have that happen.

[43:46] **Vinnie**: And it sounds like, it sounds like you have done a very good job of overcoming this. And for somebody that, I think that is someone who's working at home and has sort of mastered that process, this may be a non-issue for you. And it, I'm again, I can only speak from personal experience because that's the only experience that I subjectively experience. But, you know, that, that is, that has definitely been a consistent issue for things I find very compelling to work on.

[44:12] **Vinnie**: And I don't know if that's, it sounds like your suggestion to eliminate distractions is definitely an apt one. And I have done, you know, I've installed every browser extension, I've done, I've done things in that regard to kind of minimize distractions. But I will, I will be creative when it comes to these sorts of distractions.

[44:33] **Vinnie**: You know, I will have the urge to clean. I will have the urge to, you know, something that wasn't a problem before all of a sudden takes priority. And that will eclipse whatever I was working on before. And this is...

[44:47] **Adam**: Boom, yeah, do you mean that like you find working at home to be a challenge because there's more things that can be these type of distractions?

[44:54] **Vinnie**: That is definitely one large problem where, you know, other, other things that I would not have to deal with in an office like, let's say, a messy room that becomes more like, I can't possibly get work done if I'm in a messy room, right? I need that, that needs to be kind of the prerequisite for me to do that. And then of course, after that, it's like, well, you know, I've already started cleaning here. So perhaps I should clean, you know, the other room or perhaps I should do this other thing before I start tackling work.

[45:23] **Vinnie**: So it becomes this, you know, artificial mountain of prerequisites that I need to tackle before I actually tackle the thing that I need to do. So that's, that's another form, perhaps a production, productive procrastination that I struggle with.

[45:36] **Vinnie**: So I don't know if you have any kind of a, I don't know if there is a magic bullet for that, but I don't know if you have any kind of techniques or things that I maybe should look into to kind of alleviate these concerns that I can't imagine I'm the only person who experienced this.

[45:56] **Adam**: So maybe just to give a quick example of how this manifests for me is, you know, I run a podcast, which means I do interviews, people come on for an interview, and an example, I interviewed these, these two guys who wrote this book called the little typer, depended typing programming language.

[46:15] **Adam**: And so I ordered their book and I was working through, super hard to understand, but a lot of like crazy interesting ideas. And because something that I really enjoy is like learning, I ended up being like, well, I got to understand this book before I interview them and kind of spent all this time working through it. But at the same time, like once I interview somebody, like there's like a process, you know, like editing things and tagging things and doing whatever. And I do not enjoy that process.

## Commitment [46:47 - 48:52]

[46:47] **Adam**: So I find that I end up like focusing in on this learning step just because it's something that I really enjoy and neglecting this other step, which is a bit of drudgery. But I think it's the human condition. Like I don't think you should be yourself up for it. I don't know.

[47:00] **Vinnie**: So what, what do you do to kind of, when you need to process that information, so you kind of go through this book because you love the learning process and you really enjoy diving deep into a concept, but when it comes time to, let's say, releasing the podcast that requires you to go through this, you know, quote-unquote drudgery that is required to kind of process that and get that all uploaded, you know, do you put on like some good music? Do you just kind of consider it a means to an end?

[47:25] **Vinnie**: I guess you consider it just part of life, which it very much is. Like how do you, or do you just kind of just put your head down, put your headphones in, and then just kind of go with it?

[47:38] **Adam**: Yeah, but I have a schedule, right? So I try to get out two episodes of my podcast a month. So that is a schedule that I'm committed to. So, so maybe that's an aspect of it that you can explore is like commitment, right?

[48:02] **Adam**: So, so maybe you really want to clean your room, but you have, you know, commitment you've set for yourself to work through X. And maybe that would be helpful. Don't, don't you?

[48:15] **Vinnie**: Yeah, I think that's, that's a really good, you know, piece of advice. And I think that I probably, I don't know if I'm in the minority for a lot of these things are things that I probably just needlessly struggle through.

[48:27] **Vinnie**: And part of it is just at the end of the day, like you said, just kind of, you know, getting through it, you know, just sort of understanding that as part of life and just knowing that, you know, having a schedule in front of you, knowing that those things take priority is really, you know, kind of important.

## Having a Schedule [48:47 - 50:37]

[48:52] **Adam**: The last time I did work in an office like somebody, somebody coming to talk to me and they're just like kind of shooting the breeze. And I'm like, "What's up?" And they're like, "Oh, like what my stand-ups right now. And I haven't done anything in the past, like since we had our last standup." I was just like, "I don't know, I got distracted to nothing." So I'm just kind of like hiding here.

[49:19] **Adam**: I mean, you know, and that was a productive person who accomplished a lot of great work and, and was a good employee. I think that sometimes, you know, sometimes, you know, you won't get stuff done, happens.

[49:30] **Vinnie**: And that's probably one of the bigger incentives for me too. I mean, I really find the little, just say the act of working at home to be much more attractive than that of working in an office, especially if you have command over your, if you are disciplined individual, like you sound like a very disciplined individual, which is, you have a very, you know, apt personality for that type of work.

[49:50] **Vinnie**: And I think that there's just so, like, a lot of, let's just say, you know, wasted water cooler talk where you just are bantering back and forth about, I don't know, the most recent show or movie or just something that's just totally evaporated into the ether. And unfortunately, that is a big part of the day-to-day.

[50:12] **Vinnie**: And when it comes to making your own schedule, you know, you can kind of alleviate a lot of that. And I find that to be a really compelling reason to work from home, especially if you, as I think everyone should, value their time and value their effort and value their energy.

[50:24] **Vinnie**: And, you know, using it on those types of things is fine as long as it's deliberate, but oftentimes it becomes too commonplace and to, to, you know, to regular where you just don't even realize it. I think...

## Water Cooler Talk [50:37 - 52:38]

[50:43] **Adam**: Yeah, but I think at the same time, one of the, one of the downsides to, to working remotely, you know, it is not having that water cooler, like that. So I know almost nothing about professional sports. So like, I have no problem that I'm no longer in a workplace where people ask me about the local sports team. Like that's fine, those, I was lost on me and just, you know, made me awkward.

[51:06] **Adam**: But I think, you know, it's, you still want to have bonding with, here, you know, the people that you work with. And maybe you just have to find different ways to do it. Like I, I hear what you're saying, but I think there is value in the water cooler space as well.

[51:17] **Vinnie**: That's interesting. And that's, I, I also don't know any of the sports ball teams or anything like that. I have zero interest in any of that. And yeah, that's, you're in good company here.

[51:28] **Vinnie**: But I think that there is definitely value in it, especially that value is probably more apparent when it's taken away. When it's everyday, the value is, it's there, it's present. Social interaction is an, is a good thing to have. We are, we are social beings. I think being exposed to, you know, other people talking about things is definitely a way for us to maintain our mental health.

[51:54] **Vinnie**: But I think when it's taken away or when, when we deliberately step away from that, we need to find ways in which to supplement that type of interaction. And the value of it really becomes much more apparent.

[52:08] **Vinnie**: But there's also, you know, like anything, like any, too much of a good thing, it is not, it's not good. And I think there's very, you know, detrimental reactions to that as well. So I think it's just, you know, about anything balanced, so I think is key. Just like with water cooler talk, optimistically, the water cooler talk wouldn't center around sports. You know, that, that would be my, my ideal, ideal water cooler talk as well.

[52:28] **Adam**: No sports, a bunch of Slack channels where people just shoot the breeze and, you know, you know, also we do like video conferences and maybe you have some time to, you know, ask people about their day. But yeah, there's a diminishing water-cooler talk for sure. But it doesn't value.

## Tim Ferriss [52:38 - 53:50]

[52:38] **Vinnie**: And on that note, I know we're kind of coming up on an hour here. And I generally like to exit the conversation with some... I don't know, familiar with the podcaster bloggers, kind of man of many talents, Tim Ferriss? Someone who's interested in bullet journaling and things like that, I kind of, you know, I thought he might have come up on your radar. Are you familiar with him?

[53:15] **Adam**: Cool.

[53:15] **Vinnie**: He, he generally, when he does these sorts of things, he has a number of questions. He recently wrote a book, I think it was called "Two Little Titans" where he kind of condensed a bunch of these, you know, people that he podcasted with and sort of gave, you know, some of these questions to.

[53:33] **Vinnie**: And I just feel it's kind of a nice way to exit the show. And I'm gonna, you know, completely rip off of his question. So thank you to Tim Ferriss for providing this to me, you know, not personally, of course. But I don't think he has copyright on any of the questions. So I'm just gonna kind of, you know, rattle them off and feel free to, you know, be as concise or elaborate as you like on these.

[53:50] **Vinnie**: The first one is, and this is probably relevant to our conversation, is when you feel overwhelmed or unfocused or have lost your focus temporarily, what do you do?

## My Brother, My Brother, and Me [53:56 - 54:46]

[54:09] **Adam**: Like comedy podcasts, there's a podcast, "My Brother, My Brother and Me." And there's just three brothers like goofing around. And I don't know, for feeling overwhelmed, which to me is kind of like, you know, your anxiety for some reason is ramped up, like hearing people just make stupid jokes that can really help.

[54:26] **Vinnie**: Interesting. Okay, so humor, humor is a really big one. And I'm, I'm mature, I've not heard of "My Brother, My Brother and Me." That's the name of the podcast. I'll to check that out.

[54:39] **Vinnie**: So question two here is: what advice would you give to a smart, driven college student about to enter the real world? And what advice should they ignore?

## Develop Skills [54:46 - 55:45]

[54:53] **Adam**: Ignore advice, just pursue what you're... I mean, I guess I would say develop skills maybe. So like we talked about taking this is like a small scale, like touch-typing is a skill, learning the program is a skill. I think skills have value more so than knowledge.

[55:15] **Vinnie**: Very insightful. I like that. That's, I think it's a really big one. And skills you have, valuable skills particularly, and ones that are cross-disciplinary, like note-taking. I think is incredibly value. That's a really good answer.

[55:29] **Vinnie**: The last question here that I ask is what is the book or books you've given most as a gift and why, or what are the one to three books that have greatly influenced your life?

[55:45] **Adam**: Oh, that's, that's a tough question.

## Book Recommendations [55:45 - 56:56]

[55:53] **Adam**: Just say I have these two books here. One is called The Bullet Journal Method, as we discuss, Ryan Carroll. I think that, you know, the method of bullet journaling is very valuable. And then I also have this book called How to Take Smart Notes: One Simple Technique to Boost Writing, Learning, and Thinking.

[56:06] **Adam**: So those are on theme, but also I would say like, just, just read something trashy that's, that's fun for you. That's what I would recommend people like just, you know, sometimes make reading about just unwinding.

[56:16] **Vinnie**: I think that's really, that's not another piece of advice that I, I really enjoying something that I need to probably take to heart because most of the reading that I focus on is, it's just a more focused on developing some sort of, you know, technique or skill, which is valuable.

[56:30] **Vinnie**: But sometimes, yeah, reading is a leisure activity too. And I think that's important to keep in the back of your mind, especially when you, especially with respect to question one, when you feel overwhelmed or unfocused.

[56:43] **Vinnie**: Cool, that's, that's great. I really enjoy the answers to those questions. And it's really been a pleasure having you on this podcast. I mean, I think there's a lot of untapped things that we've really didn't even get a chance to talk about.

[56:56] **Vinnie**: We had a brief, you know, kind of touch point prior to this conversation. And there were some other topics that's maybe we'll have to kind of say for another podcast or alternatively, as you have a podcast, I don't know if you, if I would fit the bill for any of the episodes that you have on the roster. But if so, I'd be an honored guest. I would be happy to appear and we can kind of, you know, take that offline and figure out if that makes sense. If not, it's been a real pleasure. I really appreciate you taking the time to chat with me today. And I'm really glad that you reached out.

[57:23] **Adam**: Yeah, it's been great. Thank you so much.

[57:29] **Vinnie**: Of course. All right. Adam, I will talk to you later. Take care.