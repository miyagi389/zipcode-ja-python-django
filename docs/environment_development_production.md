Deploy the app (Production)
====

ローカルマシン上に軽量な開発用ウェブサーバを立ち上げて開発環境を構築する手順を記述する。


```
heroku create

git push heroku master

heroku ps:scale web=1

heroku run python app/manage.py migrate

# import tokyo zipcode
heroku run python app/manage.py import_zipcode_jp --include_zipcode_regex "^1[0-9]{6}"

heroku open
```
