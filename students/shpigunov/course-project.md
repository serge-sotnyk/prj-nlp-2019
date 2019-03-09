# Course Project Proposals
_Anton Shpigunov_

I have two topic candidates for my course project – one that is more practical, and another one more creative and fun.

## Idea 1. Corpus-Based Translation Resources

My first idea is to attempt to develop tools and resources that could improve the speed, quality and consistency of written translation within a specified domain using a parallel corpus of pre-existing translations.

Simply put, what can we do with previously translated content to help translation of the next content in the same domain?

### Goals

The goals of this project, sorted by ascending complexity, are as follows:

1. **Terminology extraction** using simple frequency analysis.
2. Building an **n-gram concordance**. For example, for the word 'terms', a common trigram would be 'terms and conditions'. This could be either used as a lookup tool, or for creation of **autosuggest dictionaries** for various translation tools.
3. seq2seq **custom machine translation model** based on previously translated content. In case the existing corpus is too small, could the model be trained on a large general corpus and then 'patched' with a smaller domain-specific one?

### Data

An available parallel corpus of 30,000+ sentences uk <--> en in the domain of wastewater treatment from one of my previous translation projects.


## Idea 2. Poetry Generation (#3 on the general list)

As I once took creative writing classes and used to write poetry back in college, this idea fascinates me and I have an interest in exploring it as an option for my course project.

Here are my initial thoughts on this idea:

Poetry, by definition, is any **text where words are arranged for beauty**. This allows a wide range of forms (the formalistic sonnet, the minimalist Japanese forms such as haiku and tanka, or the unconstrained vers libre, to name a few) and topic matters (from historical ballads to love poetry to obscure futurism, etc.)

Given this variety, here are a few exploratory questions for consideration:

### Analysis:

* Can we detect poetry using a rule-based or ML approach?
* What constitutes poetic style? What makes, say, Poe and Whitman (or Taras Shevchenko and Lesia Ukraïnka, for that matter) different?
* Would it be possible to classify poetic texts by authorship? What features would be sufficient?

### Generation:

* Can we **generate poetic-sounding text** with Markov chains or a more advanced approach using pre-existing corpora? How poetic-sounding will it be, if unconstrained?
* Can we **impose constraints** on our generated text in terms of form (meters, syllable counts or rhyme) and content (using only nature-related language, avoiding words originating later than a specific date, etc.)?
* Is it practicable to **search for a quantitative measure of poetic beauty** (using Goodreads scores, ratings of poetry posts on Deviantart, other poetry/art communities etc. -- this could be difficult to find)?
* Finally, can we constrain the generator to attempt to **maximize quantitative 'beauty'** of the texts it generates?

### Possible Data Sources

* Gutenberg Poetry Corpus
* Self-made corpora scraped from DeviantArt or other [poetry sites](https://medium.com/@sarahbaylor/8-proven-poetry-websites-to-read-and-share-your-poems-aa496e420d2d)
* [Poetry Foundation](https://www.poetryfoundation.org)