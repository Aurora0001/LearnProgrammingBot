# Training

To train the bot, you need to install LearnProgrammingBot and its dependencies (see the Installation and Setup sections).

## Training with one Specific Post
 You can train the bot with one post if it has misclassified it, using the following command:
 
     ./main.py train --id ID
     
 Where ID is the reddit submission ID, for example:
 
    https://www.reddit.com/r/learnprogramming/comments/4g4far/meta_i_wrote_a_bot_for_rlearnprogramming_that/
                                                      ^^^^^^^
In this link, the id is **4g4far**, so you could train it with:

    ./main.py train --id 4g4far
    
LearnProgrammingBot will then fetch the post from reddit, and display it for you to review. It will then prompt you to enter the correct classification of the post. Currently, there are three post categories (but this is going to change, see [#2](https://github.com/Aurora0001/LearnProgrammingBot/issues/2)):

- 'faq' - Posts that are answered on the FAQ
- 'bad' - Posts that are clearly formatted badly or unsuitable for /r/learnprogramming (e.g. blog posts that don't seem relevant)
- 'good' - Everything else!

For the best results, it's best to be generous with your classification, and, if in doubt, classify as 'good'. Check `data.db` for examples of how previous posts were classified, if you're not sure.

## Training in Batches
 You might find it easier to train with larger samples from the 'new' feed of /r/learnprogramming. This will be supported soon ([see issue #3](https://github.com/Aurora0001/LearnProgrammingBot/issues/3)).