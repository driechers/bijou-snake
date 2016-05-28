import MySQLdb

class SqlManager(object):
	def __init__(self):
		self.db=MySQLdb.connect(host="sql5.freemysqlhosting.net",
					user="sql5121329",
					passwd="plZ32PPAe4",
					db="sql5121329")

	def userIsValid(self, username):
		cursor = self.db.cursor()

		cursor.execute("SELECT id from user where name=%s",(username,))
		data = cursor.fetchall()

		cursor.close()

		if len(data) == 0:
			return False

		return True

	# Returns list of Tuples with username at 0, max len at 1
	def getTopLongest(self, n):
		cursor = self.db.cursor()

		cursor.execute("select user.name,snake.maxLen from snake left join user on user.id=snake.user_id order by maxLen desc limit %s", (n,))
		data = cursor.fetchall()

		cursor.close()

		return data

	# Returns list of Tuples with username at 0, score at 1
	def getTopFinal(self, n):
		cursor = self.db.cursor()

		cursor.execute("select user.name,snake.finalLen from snake left join user on user.id=snake.user_id order by finalLen desc limit %s", (n,))
		data = cursor.fetchall()

		cursor.close()

		return data

	# Returns list of Tuples with username at 0, number of deaths at 1
	def getTopDeaths(self, n):
		cursor = self.db.cursor()

		cursor.execute("select user.name,snake.deaths from snake left join user on user.id=snake.user_id order by deaths desc limit %s", (n,))
		data = cursor.fetchall()

		cursor.close()

		return data

	def addScore(self, username, maxLen, finalLen, deaths):
		cursor = self.db.cursor()

		try:
			cursor.execute("""
				insert into snake
				(user_id,maxLen,finalLen,deaths)
				values (
					(select id from user where name=%s)
					,%s,%s,%s)""",
					(username, maxLen, finalLen, deaths))

			self.db.commit()
		except:
			self.db.rollback()

		cursor.close()

