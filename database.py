from sqlite3 import connect
conn = connect("fountain_database.db")
cursor = conn.cursor()

class SourceSave:
	"""Class: SourceSave
	@params
	website: website name of source
	sourceName: name of source
	sourceLink: link to the source
	sourceFreqList: frequency list produced based from source
	"""
	def __init__(self, website: str, sourceName: str, sourceLink: str, sourceFreqList: str):
		self.l = sourceLink
		self.output = [website, sourceName, sourceLink, sourceFreqList]

class Record:
	"""Class: Record
	@params
	webster: webster save
	britannica: britannica save
	dictionary: dictionary.com save
	bitesize: BBC bitesize save
	wikipedia: wikipedia save
	sparknotes: sparknotes save
	booksummary: BookSummary.net save
	history: history.com save
	reuters1: first reuters save
	reuters2: second reuters save
	reuters3: third reuters save
	reuters4: fourth reuters save
	scholar1: first google scholar save
	scholar2: second google scholar save
	scholar3: third google scholar save
	scholar4: fourth google scholar save
	further1: first further reading save
	further2: second further reading save
	further3: third further reading save
	further4: fourth further reading save
	"""
	def __init__(self, 
	webster: SourceSave, britannica: SourceSave, dictionary: SourceSave, bitesize: SourceSave,
	wikipedia: SourceSave, sparknotes: SourceSave, history: SourceSave, booksummary: SourceSave,
	reuters1: SourceSave, reuters2: SourceSave, reuters3: SourceSave, reuters4: SourceSave, 
	scholar1: SourceSave, scholar2: SourceSave, scholar3: SourceSave, scholar4: SourceSave, 
	further1: SourceSave, further2: SourceSave, further3: SourceSave, further4: SourceSave
				):
		self.tblSave = [ (webster.output), (britannica.output), (dictionary.output), (bitesize.output), 
						(wikipedia.output), (sparknotes.output), (history.output), (booksummary.output),
						(reuters1.output), (reuters2.output), (reuters3.output), (reuters4.output), 
						(scholar1.output), (scholar2.output), (scholar3.output), (scholar4.output), 
						(further1.output), (further2.output), (further3.output), (further4.output)]

def create_tables():
	"""Function: create_table
	 @ 
    Creates the tblSave and tblSource tables via SQL queries to 'fountain_database.db'.
    """
	try:
		cursor.execute("CREATE TABLE tblSave (SaveID UNSIGNED INTEGER(8), Query TEXT, PRIMARY KEY (SaveID))")
		cursor.execute("CREATE TABLE tblSource (SaveID UNSIGNED INTEGER(8), Website TEXT, Name TEXT, Link TEXT, FreqList TEXT, PRIMARY KEY (SaveID, Website))")
	except:
		#tables have already been created
		pass

def reset_tables():
	"""Function: reset_table
	 @ 
   	Deletes and then recreates the tblSave and tblSource tables via SQL queries to 'fountain_database.db'.
    """
	cursor.execute("""DROP TABLE IF EXISTS tblSave""")
	cursor.execute("""DROP TABLE IF EXISTS tblSource""")
	create_tables()
	conn.commit()

def remove_record(save_number: int):
	"""Function: remove_record
	@params
	save_number: the SaveID of the record to be removed

    Deletes a specific record from the 'fountain_database.db', from both the tblSave and tblSource tables.
	It then bumps all of the SaveIDs down by one that are above the removed value's SaveID, thereby stopping the gap between saved values.
    """
	with conn:
		keyfield = "'" + str(save_number) + "'"
		cursor.execute("DELETE FROM tblSave WHERE SaveID = " + keyfield)
		cursor.execute("DELETE FROM tblSource WHERE SaveID = " + keyfield)
		cursor.execute("UPDATE tblSave SET SaveID = SaveID - 1 WHERE SaveID > " + keyfield)
		cursor.execute("UPDATE tblSource SET SaveID = SaveID - 1 WHERE SaveID > " + keyfield)

def make_save(save: Record, query: str):
	"""Function: make_save
	@params
	save: the save values to be input into the table
	query: the search query inputted to get said save values

    Inputs save values from a save Record into 'fountain_database.db' via SQL queries.
    """
	currentID = find_currentID()
	cursor.execute("INSERT INTO tblSave (SaveID, Query) VALUES (?, ?)", (currentID, query) )
	for i in save.tblSave:
		cursor.execute("INSERT INTO tblSource (SaveID, Website, Name, Link, FreqList) VALUES (?, ?, ?, ?, ?)", (currentID, str(i[0]), str(i[1]), str(i[2]), str(i[3])) )
	conn.commit()

def get_save_values():
	"""Function: get_save_values
	 @ 
	Queries the 'fountain_database.db' via an SQL query to retrieve all of the Save values.
    """
	table_output = []
	for row in cursor.execute("SELECT * FROM tblSave"):
		table_output.append(row[1])
	return table_output

def output_saved_to_table():
	"""Function: output_saved_to_table
	@ 
    Takes save values from the database and converts them into a list of length 256.
	With any extra values being removed and more blank items being added otherwise.
	"""
	save_values = [get_save_values()]
	output_values = []
	for i in save_values:
		for j in i:
			output_values.append([j])
	while int(len(output_values)) != 256:
		if int(len(output_values)) < 256:
			output_values.append([" "])
		elif int(len(output_values)) > 256:
			output_values.pop()
	return output_values

def load_save(saveID: int):
	"""Function: load_save
	@params
	saveID: the numerical ID of the save to load

    Retrieves and outputs all of the values under the same SaveID.
	"""
	pass
	keyfield = "'" + str(saveID) + "'"
	output = []
	websites = [
		"webster",
		"britannica",
		"dictionary",
		"bitesize",
		"wikipedia",
		"sparknotes",
		"booksummary",
		"history",
		"reuters1",
		"reuters2",
		"reuters3",
		"reuters4",
		"scholar1",
		"scholar2",
		"scholar3",
		"scholar4",
		"further1",
		"further2",
		"further3",
		"further4"
	]
	for w in websites:
		website = "'" + w + "'"
		for row in cursor.execute("SELECT * FROM tblSource WHERE Website = " + website + " AND SaveID = " + keyfield):
			source = SourceSave(row[1], row[2], row[3], row[4])
			output.append(source)
	save = Record(output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15], output[16], output[17], output[18], output[19])
	return save

def find_currentID():
	"""Function: find_currentID
	 @ 
    Uses an SQL query of the length of the list in order to find the next SaveID to be saved to.
	"""
	count = []
	for row in cursor.execute("SELECT COUNT(SaveID) FROM tblSave"):
		count.append(row)
	currentID = str(count[0]).replace(",", "")
	currentID = currentID.replace("(", "")
	currentID = int(currentID.replace(")", ""))
	return currentID

def list_all_data():
	"""Function: list_all_data
	 @ 
    Prints all of the data from the 'fountain_database.db' into the terminal.
	For testing purposes.
	"""
	for row in cursor.execute("SELECT * FROM tblSave"):
		print (row) 
	for row in cursor.execute("SELECT * FROM tblSource"):
		print (row)
