import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

document1 = tb("""I accidentally committed the wrong files to Git, but I haven't pushed the commit to the server yet.

How can I undo those commits from the local repository?""")

document2 = tb(""" git commit -m "Something terribly misguided"             # (1)
$ git reset HEAD~                                          # (2)
<< edit files as necessary >>                              # (3)
$ git add ...                                              # (4)
$ git commit -c ORIG_HEAD                                  # (5)
This is what you want to undo.
This does nothing to your working tree (the state of your files on disk), but undoes the commit and leaves the changes you committed unstaged (so they'll appear as "Changes not staged for commit" in git status, so you'll need to add them again before committing). If you only want to add more changes to the previous commit, or change the commit message1, you could use git reset --soft HEAD~ instead, which is like git reset HEAD~2 but leaves your existing changes staged.
Make corrections to working tree files.
git add anything that you want to include in your new commit.
Commit the changes, reusing the old commit message. reset copied the old head to .git/ORIG_HEAD; commit with -c ORIG_HEAD will open an editor, which initially contains the log message from the old commit and allows you to edit it. If you do not need to edit the message, you could use the -C option.
Beware however that if you have added any new changes to the index, using commit --amend will add them to your previous commit.

If the code is already pushed to your server and you have permissions to overwrite history (rebase) then:

git push origin master --force
You can also look at this answer:

How to move HEAD back to a previous location? (Detached head) & Undo commits

The above answer will show you git reflog which is used to find out what is the SHA-1 which you wish to revert to. Once you found the point to which you wish to undo to use the sequence of commands as explained above.""")

document3 = tb("""Undoing a commit is a little scary if you don't know how it works. But it's actually amazingly easy if you do understand.

Say you have this, where C is your HEAD and (F) is the state of your files.

   (F)
A-B-C
    ↑
  master
You want to nuke commit C and never see it again. You do this:

git reset --hard HEAD~1
The result is:

 (F)
A-B
  ↑
master
Now B is the HEAD. Because you used --hard, your files are reset to their state at commit B.

Ah, but suppose commit C wasn't a disaster, but just a bit off. You want to undo the commit but keep your changes for a bit of editing before you do a better commit. Starting again from here, with C as your HEAD:
   (F)
A-B-C
    ↑
  master
You can do this, leaving off the --hard:

git reset HEAD~1
In this case the result is:

   (F)
A-B-C
  ↑
master
In both cases, HEAD is just a pointer to the latest commit. When you do a git reset HEAD~1, you tell Git to move the HEAD pointer back one commit. But (unless you use --hard) you leave your files as they were. So now git status shows the changes you had checked into C. You haven't lost a thing!

For the lightest touch, you can even undo your commit but leave your files and your index:

git reset --soft HEAD~1
This not only leaves your files alone, it even leaves your index alone. When you do git status, you'll see that the same files are in the index as before. In fact, right after this command, you could do git commit and you'd be redoing the same commit you just had.

One more thing: Suppose you destroy a commit as in the first example, but then discover you needed it after all? Tough luck, right?

Nope, there's still a way to get it back. Type git reflog and you'll see a list of (partial) commit shas (that is, hashes) that you've moved around in. Find the commit you destroyed, and do this:

git checkout -b someNewBranchName shaYouDestroyed
You've now resurrected that commit. Commits don't actually get destroyed in Git for some 90 days, so you can usually go back and rescue one you didn't mean to get rid of.
""")

bloblist = [document1, document2, document3]
for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))


