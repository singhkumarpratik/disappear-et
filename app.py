from flask import Flask,render_template,url_for, request, send_from_directory
from firebase import firebase
from form import Firebase_Input
import secrets
import json

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = '794b86bced881103146534707eb9ea29'
@app.route('/')
@app.route('/', methods=['POST'])
def hello_world():
    form = Firebase_Input()

    if request.method == 'POST':
        firebase_var = firebase.FirebaseApplication('https://self-destruct-fef93.firebaseio.com/', None)
        urltoken = secrets.token_hex(32)
        result = firebase_var.get('/allkeys',None)
        uniqueurl = isUniqueUrl(urltoken, result)
        url = 'https://self-destruct-fef93.firebaseio.com/' + str(uniqueurl) + '/'
        firebase_var.put(url,'code', form.code.data)
        firebase_var.put('https://self-destruct-fef93.firebaseio.com/allkeys', str(uniqueurl), 1)
        generatedURL= request.url+str(urltoken)
        return render_template('generate.html',generatedURL=generatedURL)

    return render_template('index.html', form=form)

def isUniqueUrl(url, result):
    if(url in result):
        url = secrets.token_hex(32)
        return isUniqueUrl(url, result)
    return url

@app.route('/<token>')
@app.route('/<token>', methods=['POST'])
def fetchMessage(token):

    newform = Firebase_Input()

    if request.method == 'POST': 
        firebase_var = firebase.FirebaseApplication('https://self-destruct-fef93.firebaseio.com/', None)
        alltoken = firebase_var.get('/allkeys', None)
        if(token in alltoken):
            result = firebase_var.get(token, None)
            posts = result["code"]
            firebase_var.delete('https://self-destruct-fef93.firebaseio.com/',token)
            firebase_var.delete('/allkeys/', token)
            return render_template('fetch.html', posts=posts)
        else:
            return render_template('404.html')

    return render_template('button.html',form=newform)

if __name__ == "__main__":
    app.run(debug=True)