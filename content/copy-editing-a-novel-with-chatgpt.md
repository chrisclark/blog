Title: Copy Editing a Novel with ChatGPT
Date: 2023-06-28
Author: Chris Clark
Slug: copy-editing-a-novel-with-chatgpt
Status: Published

My wife, a writer, recently and unexpectedly needed a final round of copy-editing on a manuscript she had written some time ago. There wasn't time to hire a professional, and even splitting it up, we couldn't get it done between the two of us fast enough.

Luckily, I know Python and have an OpenAI API key! Thus, I asked ChatGPT to copy-edit the book. I believed this was in ChatGPT's wheelhouse for a few reasons:

1. Copy-editing is about true errors; spelling, grammar, etc. So "chunks" of text can be copy-edited separately. The entire novel doesn't need to be in the model's context window. Searching for plot holes or timeline inconsistencies in a novel-length text would be another matter entirely.
2. ChatGPT has impeccable spelling and grammar. Therefore I assumed it would be good at catching errors in text.
3. It's easy to provide good examples. "Few shot" prompting tends to improve performance.

Below we'll look at the approach I took, and the results. I've included illustrative, but incomplete, code. [Full code is available here](https://gist.github.com/chrisclark/612ab8fa9c4c6dd5a85c1529162e0efd). I used GPT4 as a coding assistant for much of this. And boy it's great. It's so nice to get working directory-traversal code (for instance) that does just what I need, without spending five minutes Googling and reading docs. GPT4-assisted Python scripting makes exercises like this much more enjoyable.

To preview the conclusion: ChatGPT performed much less well than I thought, but still provided a usable copy editing pass. It is significantly better than nothing, but surprisingly noisy and erratic.

## Chunking up the text

Using some handy ChatGPT-provided code, I chunked the novel into separate text files of (in this case) at most 1000 words. This is well under the maximum GPT4 context size of 8000 tokens (1000 words is perhaps 1250 tokens), but I found that smaller chunks lead to more consistency in finding true errors.

Separate files made downstream experimentation easier (I could delete all but a few chunks; I could write resume code when the openai API failed, etc). The chunking is deterministic and fast.

## Copy Editing with ChatGPT

Now we send the chunks to Openai and ChatGPT. The prompt below works...OK. I should have perhaps provided more rigorous few-shot examples. Nonetheless, I experimentally determined that the examples below did lend considerable consistency to the output. Without it, ChatGPT will come up with different ways of providing the feedback for each chunk, which makes the results hard for a human to process, and a machine to parse (more on that later). If I did this again, I'd spend another iteration or two on the prompt. I do believe there is quality juice to squeeze there.

> You are a copy editor looking for issues in a novel before it is submitted to publishers. You are looking for obvious grammar and spelling issues and any information that is obviously incorrect. Do not make suggestions related to style, or edits for clarity. Just focus on copy errors.

> Please format your responses as a series of bullet points. Start with a quote of a few words from the novel that you are copy-editing (so it's easy to find in the novel), then follow with your comments/corrections.

> Here are some examples of good copy edits:

> * "an two hundred year" -> "a two hundred year"
> * "on to the veranda" -> "onto the veranda"
> * "full memory of the night" -> "full memories of the night"
> * "Her and Luis's dog" -> "Her and Luis' dog"
> * "Felicia stiffened almost indecipherably." -> "Felicia stiffened almost imperceptibly."
> * "The is the family kitchen." -> "This is the family kitchen."

> Do not suggest substitutions of one type of punctuation mark for another. For example, do not suggest replacing ` with ', or “ with ".

Looping through each of the 104 chunks with GPT4 took about 35 minutes and cost just over $8 in API fees. In retrospect, for this task, I suspect GPT3.5 could give equivalent results more quickly, at less cost.

## Initial Result

So...does it work? Not as well as I'd hoped. Perhaps 1/3 of the suggestions are legitimate suggestions/corrections. The others fall into one of three categories:

1. Non-corrections. The original text and the new text are identical, or simply changed a quote or apostrophe type.
    - "I didn’t tell the police." -> "I didn't tell the police."
2. Oddly specific stylistic suggestions (in spite of the prompt asking to avoid these):
    - "She yelped. Savvy tried to apologize" -> "She yelped, and Savvy tried to apologize"
3. Total hallucinations. This text, for instance, simply doesn't appear in the corresponding chunk:
    - "highway ears as they passed" -> "highway ears as it passed"

Trying to read through an output riddled with false-positives is mentally exhausting. Which of these are legitimate suggestions and which contain no signal?

- "bulletproof glass partition. “You" -> "bulletproof glass partition, "You"
- "Detective Moorehead, please,” Savvy" -> "Detective Moorehead, please," Savvy"
- "loudly banging each letter" -> "loudly, banging each letter"
- "Finished. Straightened a stack" -> "Finished, straightened a stack"
- "What is this in" -> "What is this in,"
- "with Detective Moorehead,” she" -> "with Detective Moorehead," she"

It's like a vision test. Yikes.

After carefully reading chatGPT's output, I wrote a function to detect hallucinations (19 of them for those keeping score at home), non-corrections, and persnickety suggestions that simply involved swapping a backtick for an apostrophe (e.g. encoding nuances).

```py
def is_real_correction(input_str):
    left_side = input_str.split('->')[0].strip(' -"').replace('’', "'").replace('“', '"').replace('”', '"')
    right_side = input_str.split('->')[1].strip(' -"').replace('’', "'").replace('“', '"').replace('”', '"')
    if left_side.endswith('"') and not right_side.endswith('"'):
        left_side = left_side[:-1]
    # full_novel_text check is for hallucinations
    if left_side != right_side and 'remove extra space' and left_side in full_novel_text:
        return f'- {left_side} -> {right_side}'
```


## Final Result

For a novel of about 90,000 words, GPT4 identified 1120 "issues", which the script above reduced to 811. I suspect feeding the corrections back into ChatGPT with a prompt to identify only real corrections could have worked -- but good old-fashioned string manipulation with Python is also plenty good. I'm not yet reaching for ChatGPT to solve all of my problems, but perhaps I am a luddite.

Of the remaining corrections, about 25% are truly legitimate corrections, 50% are somewhat random wording and stylistic changes, and the remaining 25% are legitimate grammar issues, but are contained within spoken dialogue or are otherwise used purposefully. If this were a copy-edit a magazine article, this last 25% would be useful, as the author would want the writing to confirm strictly to a standard (e.g. Chicago Manual of Style) -- but is of limited utility in the context of a novel.

Here are some representative corrections.

Legitimate Copy Errors

- Felicia stiffened almost indecipherably. -> Felicia stiffened almost imperceptibly.
- The is the family kitchen. -> This is the family kitchen.
- "No, doesn’t mean that" -> "No, it doesn't mean that"

Debatable Copy Corrections

- "His laugh was contagious and his spirit big, I'm told.” -> "His laugh was contagious, and his spirit was big, I'm told.”
- "Not exactly the apology Savvy was expecting" -> "Not exactly the apology Savvy expected"

Arbitrary Rephrasings

- "He stood on the opposite side" -> "He stood on the other side"
- "He put his glass down" -> "He set his glass down"
- "the overhead lights flashed" -> "the overhead lights flickered"
- "The corners of his mouth" -> "The corners of his lips"


## Conclusion

Yeah - I mean - not bad? Kind of OK for $8? (Ignoring the ~2 hours of time it took me to wrangle the code)

I can't help but feel a little disappointed, as this felt like a slam-dunk for ChatGPT. As the [old saying goes](https://cdixon.org/2009/08/20/machine-learning-is-really-good-at-partially-solving-just-about-any-problem), AI is great at solving 80% of any problem.

With that said, I do think ChatGPT (or even a much simpler model) could be turned into an excellent copywriter through fine tuning. The tech is surely capable of doing much better. Given some more time, I would have loved to try that approach (especially because training data is easy to generate for this use case). Perhaps in a future blog post...
