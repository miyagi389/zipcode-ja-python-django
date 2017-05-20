Deploy the app (Production)
====

```
heroku create

git push heroku master

heroku ps:scale web=1

heroku run python app/manage.py migrate

# import tokyo zipcode
heroku run python app/manage.py import_zipcode_jp --include_zipcode_regex "^1[0-9]{6}"

heroku open
```
