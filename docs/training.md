# Training

To train the bot, you need to install LearnProgrammingBot and its dependencies (see the Installation and Setup sections).

## Training with a Specific Post
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
 
## Committing Changes
 To merge your database changes with the main repository, [fork LearnProgrammingBot](https://github.com/Aurora0001/LearnProgrammingBot) on GitHub, then clone your copy. Train the classifier using the steps listed above, then [create a pull request](https://help.github.com/articles/using-pull-requests/). Try to do this relatively quickly (i.e. don't wait for days before merging) because it's difficult to resolve merge conflicts with the database.
 
### Summary
1. Fork repository
2. `git clone https://github.com/MyUserName/LearnProgrammingBot`
3. Train classifer
4. `git commit -m "Trained classifier with X new records"`
5. `git push origin master`
6. Create pull request on GitHub