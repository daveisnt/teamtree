import pandas as pd
import os.path
from django.http import HttpResponse

def index(request):
	
	return HttpResponse('<html><head><meta http-equiv="refresh" content="0; URL=/tree/Petrovic,%20Bob/"></head></html>')

def detail(request,name):

	output = "<html>"
	
	def topBoss(df):
		return df.loc[df['Manager Name'].isnull()]['Individual Name'].tolist()[0]

	def getBoss(name, df):
		return df.loc[df['Individual Name'] == name]['Manager Name'].tolist()[0]

	def getReports(name, df):
		return df.loc[df['Manager Name'] == name]['Individual Name'].tolist()

	def getPeers(name, df):
		return getReports(getBoss(name,df),df)
		
	def errorHandler(code):
		header = "<html><body><p style='font-family:Arial;font-size:18px;text-decoration:none'><b>Error: </b>"
		footer = "</p></body></html>"
		errors = pd.Series(data={'no_teamtree':'teamtree.csv not found.',
								 'no_teamupdates':'teamupdates.csv not found.',
								 'no_first':'The "Team Member First Name" field is missing from teamtree.csv',
								 'no_last':'The "Team Member Last Name" field is missing from teamtree.csv',
								 'no_manager':'The "Manager Name" field is missing from teamtree.csv',
								 'no_email':'The "Team Member Email" field is missing from teamtree.csv',
								 'no_timezone':'The "Time Zone" field is missing from teamtree.csv',
								 'no_test':'The "Test" field is missing from teamtree.csv',
								})
		return header+errors[code]+footer
		
	def printLn(st, output, indent):
		email = df_team[df_team['Individual Name']==st]['Team Member Email'].to_list()[0]
		first = df_team[df_team['Individual Name']==st]['Team Member First Name'].to_list()[0]
		last = df_team[df_team['Individual Name']==st]['Team Member Last Name'].to_list()[0]
		role = df_team[df_team['Individual Name']==st]['Role'].to_list()[0]
		tz = str(df_team[df_team['Individual Name']==st]['Time Zone'].to_list()[0])
		tabs = ""
		for i in range(0,indent):
			tabs = "&emsp;" + tabs
		a =     tabs + "<a style='font-family:Arial;font-size:18px;text-decoration:none;color:#4b286d;' href='/tree/"+st+"'><b>"+first+" "+last+"</b></a><p style='font-family:Arial;font-size:18px; display:inline'>, "+role+"</p><br>"
		a = a + tabs + "<a style='font-family:Arial;font-size:12px;text-decoration:none;color:#4b286d;' href='mailto:"+email+"'>"+email+"</a><p style='font-family:Arial;font-size:10px; display:inline'>  ("+tz+")<br></p>"
		return output + a + "<br>"

	def applyUpdates(df_updates, df_team):
		df_updates = df_updates.fillna('')
		df_updates['Individual'] = df_updates['Last'] + ', '+df_updates['First']
		for i,row in df_updates.iterrows():
			name = row['Individual']
			role = row['Role']
			manager = row['Manager']
			email = row['Email']
			if (df_team[df_team['Individual Name'] == name]['Individual Name'].count() == 0):
				# Adding a new team member
				df_team = df_team.append({'Team Member Last Name':row['Last'], 
								'Team Member First Name':row['First'], 
								'Team Member Email':email, 
								'Manager Name':manager, 
								'Individual Name':name, 
								'Role':role, 
							},ignore_index=True)
			else:
				if (role != ""):
					df_team.loc[df_team['Individual Name']==name,'Role'] = role
				if (manager != ""):
					df_team.loc[df_team['Individual Name']==name,'Manager Name'] = manager
				if (email != ""):
					df_team.loc[df_team['Individual Name']==name,'Team Member Email'] = email
		return df_team

	# Load team list
	if not os.path.isfile('teamtree.csv'):
		return HttpResponse(errorHandler('no_teamtree'))
	df_team = pd.read_csv('teamtree.csv', low_memory=False)
	if not 'Team Member First Name' in df_team.columns:
		return HttpResponse(errorHandler('no_first'))
	if not 'Team Member Last Name' in df_team.columns:
		return HttpResponse(errorHandler('no_last'))
	if not 'Team Member Email' in df_team.columns:
		return HttpResponse(errorHandler('no_email'))
	if not 'Time Zone' in df_team.columns:
		return HttpResponse(errorHandler('no_timezone'))
	if not 'Manager Name' in df_team.columns:
		return HttpResponse(errorHandler('no_manager'))
	df_team['Individual Name'] = df_team['Team Member Last Name'] + ', '+df_team['Team Member First Name']
	df_team['Role'] = ""

	# One-time fix 
	df_team.replace('Raines, John Mitchell', 'Raines, John', inplace=True)

	# Apply team list updates
	if not os.path.isfile('teamupdates.csv'):
		return HttpResponse(errorHandler('no_teamupdates'))
	df_updates = pd.read_csv('teamupdates.csv', low_memory=False)
	df_team = applyUpdates(df_updates, df_team)

	searchName = name
	indent = 0
	
	# If search name not found or no name was specified, default to top boss
	if (df_team[df_team['Individual Name'] == searchName]['Individual Name'].count() == 0):
		searchName = topBoss(df_team)
	if (searchName == ""):
		searchName = topBoss(df_team)
	
	# Generate list of bosses
	bosses = []
	if (searchName != topBoss(df_team)):  #If I didn't search by top boss
		bossname = getBoss(searchName,df_team)
		while (bossname != topBoss(df_team)):
			bosses.insert(0,bossname)
			bossname = getBoss(bossname,df_team)
		bosses.insert(0,topBoss(df_team))
	
	# Print list of bosses
	for i in bosses:
		output = printLn(i, output, indent)
		indent = indent + 1

	# Print name of individual
	output = printLn(searchName, output, indent)
	indent = indent + 1

	#Print list of reports
	for i in getReports(searchName, df_team):
		output = printLn(i, output, indent)
	
	output = output + "</html>"
	
	return HttpResponse(output)
	