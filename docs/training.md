# Training

To train the bot, you need to install LearnProgrammingBot and its dependencies (see the Installation section). You do **not** need to create OAuth tokens as shown in the Setup section if you are only training the bot.

## Training with a Specific Post
 You can train the bot with one post if it has misclassified it, using the following command:

     ./main.py train --id ID

 Where ID is the reddit submission ID, for example:

    https://www.reddit.com/r/learnprogramming/comments/4g4far/meta_i_wrote_a_bot_for_rlearnprogramming_that/
                                                      ^^^^^^^
In this link, the id is **4g4far**, so you could train it with:

    ./main.py train --id 4g4far

LearnProgrammingBot will then fetch the post from reddit, and display it for you
to review. It will then prompt you to enter the correct classification of the
post. Here are the categories (an updated list is found in `review_corpus.py`)

Valid categories:
- good
- off_topic (incl. bad questions)
- faq_get_started (incl. getting started with a project - where do I start?)
- faq_career
- faq_resource (incl. challenges e.g. codewars)
  - faq_resource_podcast
- faq_tool (incl. laptop specs)
- faq_language (e.g. how much should I know before I am expert, which should I
pick)
- faq_other (including motivation, 'does a programmer google?', project ideas etc.)
- faq_what_now (what to do after codecademy etc.)

For the best results, it's best to be generous with your classification, and, if in doubt, classify as 'good'. Check `data.db` for examples of how previous posts were classified, if you're not sure.

## Training in Batches
 You might find it easier to train with larger samples from the 'new' feed of /r/learnprogramming. This is supported with the `train-batch` command, which can be used like so:

     ./main.py train-batch --limit AMOUNT_OF_POSTS_TO_CLASSIFY

 This is also interactive, just like the `train` command. To see the valid classifications, please see the above section.

## Committing Changes
 To merge your database changes with the main repository, [fork LearnProgrammingBot](https://github.com/Aurora0001/LearnProgrammingBot) on GitHub, then clone your copy. Train the classifier using the steps listed above, then [create a pull request](https://help.github.com/articles/using-pull-requests/). Try to do this relatively quickly (i.e. don't wait for days before merging) because it's difficult to resolve merge conflicts with the database.

### Summary
1. Fork repository
2. `git clone https://github.com/MyUserName/LearnProgrammingBot`
3. Train classifer
4. `git commit -m "Trained classifier with X new records"`
5. `git push origin master`
6. Create pull request on GitHub
