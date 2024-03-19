from flask import Flask,render_template,request,session,redirect,url_for,jsonify,send_file
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
import re,os
from moviepy.editor import ImageSequenceClip, AudioFileClip,concatenate_videoclips
from PIL import Image
import os
from maker import images_to_video
# from sqlalchemy import create_engine, text
import psycopg2
# conn = psycopg2.connect(os.environ["DATABASE_URL"])

def connect_to_database():
    conn_params = {
        'host': 'cross-phoenix-8908.8nk.gcp-asia-southeast1.cockroachlabs.cloud',
        'port': 26257,
        'user': 'shubham',
        'password': 'M9N5abn1L4MqemR-fg7-zQ',
        'database': 'user_database',
        'sslmode': 'verify-full',
        'sslrootcert': 'root.crt' # Replace with the correct path
    }

    conn_str = "host={host} port={port} user={user} password={password} dbname={database} sslmode={sslmode} sslrootcert={sslrootcert}".format(**conn_params)

    # Connect to the database
    try:
        conn = psycopg2.connect(conn_str)
        return conn
    except psycopg2.OperationalError as e:
        return None


# global variables
HEIGHT = 600
WIDTH = 900

# engine = create_engine(os.environ["DATABASE_URL"])
# engine = create_engine("cockroachdb://shubham:M9N5abn1L4MqemR-fg7-zQ@cross-phoenix-8908.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/user_database?sslmode=disable")
# conn = engine.connect()



app = Flask(__name__)

app.secret_key = 'your secret key'

UPLOAD_FOLDER = 'uploads'  # Folder where uploaded images will be stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed image file extensions

#app configurations
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='password'
# app.config['MYSQL_DB']='user_database'

# mysql=MySQL(app)

conn=connect_to_database()
print(conn)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login' , methods=['GET','POST'])
def login():
    user_email = session.get('email')
    if user_email:
        cursor=conn.cursor()
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_info WHERE email = %s', (user_email,))
        account = cursor.fetchone()
        if account:
             return  redirect(url_for('workarea'))

    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM user_info WHERE email = %s AND password = %s', (email, password))

        account = cursor.fetchone()
        print(account)
        if account:
            
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[2]
            session['name']=account[1]
            msg = 'Logged in successfully !'
            return  redirect(url_for('workarea'))
          
        else:
            
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():

        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        session.pop('name',None)
        return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor=conn.cursor()
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_info WHERE name = %s', (name, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers !'
        elif not name or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user_info (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
            # mysql.connection.commit()
            conn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

@app.route('/workarea')
def workarea():
    # cursor = mysql.connection.cursor()
    cursor=conn.cursor()
    cursor.execute("SELECT image_path,image_id FROM image_data where user_id= %s",(session['id'],))
    image_path = cursor.fetchall()
    cursor.close()
    # return f"{image_path[0][1]}"                                           
    return render_template('workArea.html', image_path=image_path, name=session['name'])
    # return f"{image_path}"










@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    uploaded_files = request.files.getlist('file')
    
    for file in uploaded_files:
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            # Save the file to the specified folder inside the 'uploads' folder
            folder_path = os.path.join('static', 'uploads',session['name'])
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            filename = os.path.join(folder_path,(file.filename))
            file.save(filename)
            
            # Get the relative path of the image
            relative_path = os.path.relpath(filename, 'static')
            file_size = os.path.getsize(filename)
            split_tup = os.path.splitext(filename)
            file_extension = split_tup[1]
            
            # Save the relative path to the database
            # cursor = mysql.connection.cursor()
            cursor=conn.cursor()
            cursor.execute("INSERT INTO image_data (image_path, user_id, image_size, image_name, image_extension) VALUES (%s, %s, %s, %s, %s)", (relative_path, session['id'], file_size, file.filename, file_extension))
            # mysql.connection.commit()
            conn.commit
            cursor.close()
        else:
            return 'Invalid file type'
    
    return redirect(url_for('workarea'))




          
@app.route('/deleteimage', methods=['POST'])
def delete_image():
    data = request.get_json()
    image_id = data.get('imageId') 
    # cursor = mysql.connection.cursor()
    cursor=conn.cursor()
    # Fetching image path from the database
    cursor.execute("SELECT image_path FROM image_data WHERE image_id=%s", (image_id,))
    image_path = cursor.fetchone()
    
    # If image path exists, delete the image file
    if image_path:
        image_path = image_path[0]  # Extracting the file path string from the tuple
        if os.path.exists(f"static/{image_path}"):
            os.remove(f"static/{image_path}")
    
    # Deleting the entry from the database
    cursor.execute("DELETE FROM image_data WHERE image_id=%s", (image_id,))
    # mysql.connection.commit()
    conn.commit()
    
    # Closing the database cursor
    cursor.close()
    
    # Redirecting to the appropriate route
    return redirect(url_for('workarea'))
   
    
@app.route('/admin')
def admin():
    # cursor = mysql.connection.cursor()
    cursor=conn.cursor()
    cursor.execute("SELECT id,name,email FROM user_info")
    user_data= cursor.fetchall()
    cursor.execute("SELECT COUNT(*) from user_info")
    user_num=cursor.fetchall()
    cursor.execute("select count(*) from image_data")
    image_num=cursor.fetchall()
    cursor.close()
    return render_template('admin.html',user_data=user_data,user_num=user_num,image_num=image_num)

from moviepy.editor import ImageSequenceClip, concatenate_videoclips, AudioFileClip
from PIL import Image
import os

@app.route('/createVideo', methods=['POST', 'GET'])
def createVideo():
    # return request.form;
    image_folder = f"static/uploads/{session['name']}"
    video_path = f"static/uploads/{session['name']}/video.mp4"
    music_path = ""
    # transition = "crossfade"  # Default transition
    fps = 10
    transition='none'
    if request.method == 'POST':
        music_path = request.form['backgroundMusic']
        transition = request.form['transition']
    print(transition)

    video_data = request.form.to_dict()
    del video_data['backgroundMusic']
    del video_data['transition']

    images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg") or img.endswith(".jpeg")]

    durations = []
    for key in sorted(video_data.keys()):
        durations.append(int(video_data[key]))
    transition_array=0;
    if transition=='none':
        transition_array=[0] * (len(images)-1)
    if transition=='crossFade':
        transition_array=[1] * (len(images)-1)
    if transition=='slideInLeft':
        transition_array=[2] * (len(images)-1)
    if transition=='slideInRight':
        transition_array=[3] * (len(images)-1)
    if transition=='slideInTop':
        transition_array=[4] * (len(images)-1)
    if transition=='slideInBottom':
        transition_array=[5] * (len(images)-1)
    


    # print(images)
    # return images

    
    

    print(transition_array)

    images_to_video(images, video_path, durations, transition_array, music_path, fps=10)

   
    return render_template('workArea.html', video_path=video_path, name=session['name'])


@app.route('/downloadVideo')
def downloadVideo():
    VIDEO_FILE_PATH=f"static/uploads/{session['name']}/video.mp4"
    return send_file(VIDEO_FILE_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)




   
if __name__=="__main__":
    app.run(debug=True,port=3000)