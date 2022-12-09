import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"
path_db = './database/tfinal.db'


def register_user(username,fullname,password,isAdmin):
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    cur.execute('INSERT INTO Users(Username,Fullname,Password,isAdmin) values (?,?,?,?)', (username,fullname,password,isAdmin))
    con.commit()
    con.close()


def check_user(username, password):
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    cur.execute('SELECT Username,Password FROM Users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False





@app.route("/")
def index():
    return render_template('login.html')


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']
        isAdmin = request.form['isAdmin']

        register_user(username, fullname,password, 0)
        return redirect(url_for('index'))

    else:
        return render_template('signup.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    else:
        return "Username or Password is wrong!"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    con = sqlite3.connect(path_db)
    cur = con.cursor()
    search = f'''SELECT Album.ArtistId, Album.title, Artist.name , Track.name
                FROM Album 
                INNER JOIN Artist
                ON Album.ArtistId = Artist.ArtistId
                INNER JOIN Track ON Album.AlbumId=Track.AlbumId;
                '''
    cur.execute(search)
    result = cur.fetchall()
    
    x = []

    for artist in result:
        data = ('id', 'album', 'artist', 'track')
        if len(artist) == len(data):
            res = {data[i] : artist[i] for i, _ in enumerate(artist)}
            x.append(res)
    
            

    dataFilter = []

    if request.method == 'POST':
        filter = request.form['fil']
        
        for result in x:
            filter = filter.upper()
            
            if result['album'].upper().startswith(filter) or result['artist'].upper().startswith(filter) or result['track'].upper().startswith(filter):

                dataFilter.append(result)    
    
    return render_template('main.html', x=x, dataFilter=dataFilter)



if __name__ == '__main__':
    app.run(debug=True)