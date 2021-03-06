What is Schemey?
================

Schemey is a subset of the Scheme language written in Python. It currently includes:

* A compiler from Scheme to Schemey VM bytecode
* An implementation of a stack-based virtual machine called "Schemey VM"
* A serializer and deserializer for Schemey VM bytecode

Schemey was created for self educational purposes. After having become interested in
language design, I decided that I wanted to implement a functional interpreter/compiler
for an already existing  language. I had already tried many times before to implement one, some for
custom languages others for already existing languages. This time however, I was determined to
stick with this project, and finish it out not matter how long it took.

I learned several different things during the project, such as:

* How to create a functional compiler.
* How to create a custom serialization & deserialization API.
* How to implement a functional virtual machine.

The reason I choose Scheme is because of its simplicity. The overall syntax of Scheme
is very simple compared to that of other languages, which makes it an excellent choice
for usage.

Since the purpose of my project was to educate, I've tried to make my code as
simple, clean, and easy to understand as possible so that others can come
along and benefit from it. Also, all code in this project is in public
domain(see *License* for more details).


What can Schemey be used for?
-----------------------------

As stated above, Schemey was written for educational purposes, and thus, Schemey's core
purpose it to be used to educate. Of course, there are many other ways
to use Schemey, and I encourage you to explore them.

One major caveat is however; Schemey is still very, very early in development
and should not - I repeat - SHOULD NOT be used in production level code and/or
software.

What Scheme does Schemey implement?
----------------------------------

Schemey implements a subset of the [`R5RS`_] - *Revised5 Report on the Algorithmic Language Scheme* - standard.
I had original planned to implement a subset of LISP, but choose Scheme instead.

However, this project was designed to be usable and modifiable, so extending the functionality of Schemey would
not be very hard. I do plan however, to occasionally update Schemey(I am not promising anything though).

.. _R5RS: http://www.schemers.org/Documents/Standards/R5RS/

What is the design philosophy behind Schemey?
---------------------------------------------

The two core design philosophies behind Schemey were,
*simplicity* and *clearness*.

From the very beginning of the project, I already knew that
I wanted to write clear, easy to understand code. Code that any
level Python programmer, could understand.

I wouldn't use complex or confusing lines of code, nor would I try to
squeeze every little drop of performance out of my code. My goal was
to create a project that was approachable by anyone. In other words,
``simplicity + clearness > performance``.
