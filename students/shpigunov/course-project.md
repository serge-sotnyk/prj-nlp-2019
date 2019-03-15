# Generation of Ukrainian Poetry
_a course project by Anton Shpigunov_

As I once took creative writing classes and used to write poetry back in college, this idea fascinates me and I have an interest in exploring it as an option for my course project.

## Goals and Definitions

The goal of this project is to create a system that would **generate poetic texts in the Ukrainian language**.

Poetry, by definition, is any **text where words are arranged for beauty**. 

This allows a wide range of forms (the formalistic sonnet, the minimalist Japanese forms such as haiku and tanka, or the unconstrained vers libre, to name a few) and topic matters (from historical ballads to love poetry to obscure futurism, etc.)

Given such variety of form, we shall define poetry as cohesive natural text that satisfies any or all of the following constraints:

* uses a **poetic meter** (i.e. a certain combination of stressed and unstressed syllables e.g. iambic pentameter, or a syllabic length form e.g. haiku);
* follows a **rhyming scheme**;
* uses **phonetic devices** such as alliteration, con- and assonance;
* etc.

## Data

As input data, we intend to use Ukrainian poetic texts that are freely published on the Web. As this is an academic project without pursuit of profit, we believe that no special licensing is required.

## Engineering Tasks

* **Generation of poetic texts** using a basic Markov chain or more advanced ML-based approaches;
* **Imposing constraints on the text**, as discussed above;
* Explore the possibility of establishing a **quantitative measure of quality** of poetic content;
* Constrain the generator to attempt to **maximize quantitative 'beauty'** of generated texts.

