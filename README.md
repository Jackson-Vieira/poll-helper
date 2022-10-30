# VotingApp 

this project is being updated

### Screenshots
![Home (no topics)](public/readme/no_topics.png)

![Create a Topic Page](public/readme/create_topic.png)

![Public Topics Page](public/readme/two_topics.png)

![Vote admin(owner) Page](public/readme/vote_page.png)

![Result Page ](public/readme/result_page.png)

### Built with
- Django
- Bootstrap5
- HTML5/CSS/JS
- Django default database (SQLite3)

### What I improved/learned
 - Authentication System (LOGIN/LOGOUT/REGISTER redirects)
 - GenericViews
 - URLs
 - Tests 
 - QuerySet API 
 - Race conditions 
 
```python
class QuestionModelTests(TestCase):
	def test_was_published_recently_with_old_question(self):
	"""
	was_published_recently() returns False for questions whose pub_date
	is older than 1 day.
	"""
	time = timezone.now() - datetime.timedelta(days=1, milliseconds=1)
	old_question = Question(pub_date=time)
	self.assertIs(old_question.was_published_recently(), False)
```

```python
LOGIN_URL = "users:login"
LOGOUT_REDIRECT_URL = LOGIN_URL
LOGIN_REDIRECT_URL = "polls:index"
```

### Improvements
[ ] - Relationship between voters and choice (One-to-Many)
[ ] - Only one vote per user
[ ] - Add filter for (owner-topics)
[ ] - Clean code (views_names, urls_names, templates_names and fields_names')
[ ] - Update detail view/template ( "bug" vote without choices )
[ ] - Not_allowed.html (response)
[ ] - Unique topics names
[ ] - Update result template (data visualization)
[ ] - Topics Tags
[ ] - Share a topic (link/qr code)

### Contribute for this project
Steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <nome_branch>`.
3. Make your changes and commit thems: `git commit -m '<mensagem_commit>'`
4. Push to original branch: `git push origin <project_name> / <local>`
5. Create the pull request.

GitHub Docs [how to create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).