# golinker
python flask web app to redirect urls from go/tgjamin to full urls like http://github.com/tgjamin/golinker

# run the flask app
```
shell$ python run.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

# using the app

go to <ip>:5000/ to get the main page to add a go/link
then you can go to http://go/foo to be redirected to the proper link

## change link
for now in order to update a link you input the alias you would like to change and submit a new long url. This will update the database and overwrite the old value. 

## DNS Setup
in order for a browser on your local network to use http://go/foo you must have dns setup. This may be as simple as having a server broadcast its hostname as go.local and having .local in your search domain. This excercise is left for the reader. 
