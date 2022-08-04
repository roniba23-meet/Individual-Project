
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDI0MmpEO9ACKA6YMZeqDDDK0V4dtalTZ4",
  "authDomain": "personal-project-d3059.firebaseapp.com",
  "projectId": "personal-project-d3059",
  "storageBucket": "personal-project-d3059.appspot.com",
  "messagingSenderId": "130589715875",
  "appId": "1:130589715875:web:68ea08f0100d3d3315be16",
  "measurementId": "G-NG1TZ7BFLR",
  "databaseURL": "https://personal-project-d3059-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
app = Flask(__name__, template_folder='templates', static_folder='static')
db= firebase.database()

app.config['SECRET_KEY'] = 'super-secret-key'

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	error=""
	if (request.method=='POST'):
		email=request.form['email']
		password=request.form['password']
		user= {"email":email, "password":password}
		login_session['user'] = auth.create_user_with_email_and_password(email, password)
		db.child('Users').child(login_session['user']['localId']).set(user)
		try:
			
			
			return redirect(url_for('add'))
		except:
			error="something"
	return render_template('signup.html')

@app.route("/", methods=["GET", 'POST'])
def signin():
	error=""
	if (request.method=='POST'):
		email = request.form['email']
		password = request.form['password']
		login_session['user'] = auth.sign_in_with_email_and_password(email, password)
		try:
			return redirect(url_for('add'))
		except:
			error = "Authentication failed"
	print("shoot")
	return render_template("signin.html")

@app.route("/add", methods=['GET', 'POST'])
def add():
	if (request.method=='POST'):
		word={
	 	"wordss":request.form['word'], 
	 	"definition":request.form['definition']}
		db.child("words").push(word)
		return redirect(url_for('home'))

	return render_template("add.html")

@app.route("/home", methods=['GET', 'POST'])
def home():	
	if True:#(request.method=='POST'):
		board=[[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "],
			[" "," "," "," "," "," "," "," "," "," "," "," "," "," "]]
			

		words=db.child("words").get().val().values()
		for line in board:
			for i in line:
				i=" "
		class Word:
			def __init__(self, word, direction, start):
				self.word=word
				self.direction=direction
				self.start=start

		list_words=["dog", "gorila", "banana", "cat", "bird", "lbla","sivan","ronit"]
		meaning = ["animal that barks","animal that grunts", "fruit", "meow", "flies","lbla",  "awesome",  "nickname",  "fruit",  "swims"]
		first=Word(list_words[0],"a", [(int)((len(board)/2)),(int)((len(board[0]))/2-len(list_words[0])/2)])
		list_obj=[first]
		for i in words:
			print("woww")
			print(i)
			#list_words.append(i[1]["wordss"])
			#meaning.append(i[0]["definition"])
		for i in range(0,len(list_words[0])):
			board[first.start[0]][first.start[1]+i]=first.word[i]
		#, "thh"]
		#print("pfopoifsdpof: ")
		#print(list_obj[0].word)
		# a function to take the index in the list_obj of one word, and the second word and return the start index for the new word
		def letter(current, index_of_connected1):
			check1 =-1
			check2=-1
			final=[]
			for m in range (0, len(current)):

				for k in range (0, len(list_obj[index_of_connected1].word)):
					if current[m]==list_obj[index_of_connected1].word[k]:
						check1= k
						check2=m
			if check1==-1:
				return -1
			else:
				if list_obj[index_of_connected1].direction=='a':
					final=[list_obj[index_of_connected1].start[0]-check2,list_obj[index_of_connected1].start[1]+check1]
					return final
				else:#if list_obj[index_of_connected1].direction=='a':
					final=[list_obj[index_of_connected1].start[0]+check1, list_obj[index_of_connected1].start[1]-check2] 
					return final

		# a function to take the index  in the list_obj of two words and add the new qord to the lists, add the word to the board
		def Add(index_of_current, index_of_connected):
			print("workeddddd")
			ch=""
			location=[int(letter(list_words[index_of_current],index_of_connected)[0]), int(letter(list_words[index_of_current],index_of_connected)[1])]
			if location!=-1:

				if (list_obj[index_of_connected].direction=='a'):
					ch='d'
					for q in range (0,len(list_words[index_of_current])):
						board[q+location[0]][location[1]]= list_words[index_of_current][q]
				else:
					ch='a'
					for q in range (0,len(list_words[index_of_current])):
						board[location[0]][q+location[1]]= list_words[index_of_current][q]
				list_obj.append(Word(list_words[index_of_current], ch, location))
			return 1
			
			
		# a function to check wether the spost of a certain location are taken or not(of it is taken, it checks wether it fits or not)
		def isFree(current1,index_of_connected2):
			location2= letter(current1, index_of_connected2)
			if location2!=-1:
				try:
					if list_obj[index_of_connected2].direction=='a':
						for r in range (0, len(current1)):
							if board[location2[0]+r][location2[1]]!=" " and current1[r]!=board[location2[0]+r][location2[1]]:
								return False
					else:
						for r in range (0, len(current1)):
							if board[location2[0]][location2[1]+r]!=" " and current1[r]!=board[location2[0]][location2[1]+r]:
								return False
						
						#for r in range (0, len(current1)):
					return True
				except:
					return False




		#first= Word(list_words[0], "", [(len(board)-len(list_words[0]))/2, (len(board[0]))/2])
		#list_obj=[first]


		for i in range (1,len(list_words)):
			try:
				for j in range(0,len(list_obj)):
					print ("trying ", list_words[i], " and ", list_obj[j].word)
					print(letter(list_words[i],j))
					print("is free?", isFree(list_words[i],j))
					if letter(list_words[i],j)!=-1:
						if isFree(list_words[i],j):
							Add(i, j)
							i=i+1
							j=0
						#elif j==i-1:
							#list_words.remove(list_words[i])
			except:
				print("shoot")


		for line in board:
			print(line)
		numbers=[]
		for i in range (0,len(list_obj)):
			numbers.append(list_obj[i].start)
		print(numbers)
		#print(letter(list_words[1],0))
		return render_template("home.html", board=board, meaning=meaning, len_board=len(board), len_line=len(board[0]), location_list=numbers)
	return render_template("home.html")
if __name__ == '__main__':
	app.run(debug=True)

