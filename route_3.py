from copy import deepcopy
# -*- coding: utf-8 -*-
global bestPath_cost
global bestPath_time
global bestPath_distance
global bestCost
global bestTime
global bestDistance


def read_file(filename):
	data=[]
	f = open(filename,'r')
	line = f.readline()
	count = -1
	while(line!=''):
		line = line.split(';')
		i=max(1,1+count)
		l=[]
		while(i<len(line)):
			s=''
			j=0
			while(j<len(line[i]) and line[i][j]!='\r' and line[i][j]!='\n'):
				s+=line[i][j]
				j+=1
			if(count==-1):
				l.append(s)
			else:
				l.append(float(s))
			i+=1
		data.append(l)
		line = f.readline()
		count+=1	
	return data


def compute_route(cities,data_cost,data_time,data_distance,path,end,curr_cost,curr_time,curr_distance,hint,level):
	global bestPath_cost
	global bestPath_time
	global bestPath_distance
	global bestCost
	global bestTime
	global bestDistance

	
	i=0
	last=level-1
		
	if(level==len(cities)-1):
		#cost	
		i=path[level]	
		j=path[last]
		if(i<j):
			c=data_cost[i][j-i]
			t = data_time[i][j-i]
			d = data_distance[i][j-i]
		else:
			c=data_cost[j][i-j]
			t = data_time[i][j-i]
			d = data_distance[i][j-i]
		curr_cost+=c
		curr_time+=t
		curr_distance+=d
		if(curr_cost<bestCost):
			bestPath_cost = deepcopy(path)
			bestCost = curr_cost
			print('cost',curr_cost,path)

		if(curr_time<bestTime):
			bestPath_time = deepcopy(path)
			bestTime = curr_time
			print('time',curr_time,path)
		if(curr_distance<bestDistance):
			bestPath_distance = deepcopy(path)
			bestDistance = curr_distance
			print('distance',curr_distance,path)

		return

	i=hint[level]
	
	while(i<len(cities)):
		if(i not in path):
			
			j=path[last]
			
			if(i<j):
				c=data_cost[i][j-i]
				t = data_time[i][j-i]
				d = data_distance[i][j-i]
			else:
				c=data_cost[j][i-j]
				t = data_time[j][i-j]
				d = data_distance[j][i-j]
		#	print("aqui",level,curr_cost+c<bestCost or curr_time+t < bestTime or curr_distance+d < bestDistance)
			if(curr_cost+c<bestCost or curr_time+t < bestTime or curr_distance+d < bestDistance):
				path[level] = i
				compute_route(cities,data_cost,data_time,data_distance,path,end,curr_cost+c,curr_time+t,curr_distance+d,hint,level+1)
				
		i+=1
	i=0
	while(i<hint[level]):
	
		if(i not in path):
			j=path[last]
			
			if(i<j):
				c=data_cost[i][j-i]
				t = data_time[i][j-i]
				d = data_distance[i][j-i]
			else:
				c=data_cost[j][i-j]
				t = data_time[j][i-j]
				d = data_distance[j][i-j]
		
			if(curr_cost+c<bestCost or curr_time+t < bestTime or curr_distance+d < bestDistance):
				path[level] = i
				compute_route(cities,data_cost,data_time,data_distance,path,end,curr_cost+c,curr_time+t,curr_distance+d,hint,level+1)
				
		i+=1
	path[level]=-1

def greedy(begin,end,data,cities):
	path=[cities.index(begin)]
	totalCost = 0.0
	visited = 1
	total = len(cities)
	current=cities.index(begin)
	while(visited<total):
		if(visited==total-1):
			#end
			i=cities.index(end)
			if(current<i):
				first = current
				second = i-first
			else:
				first = i
				second = current-first
			path.append(cities.index(end))
			totalCost += data[first][second]
			return path,totalCost
		cost=9999
		for i in range(len(cities)):
			if(cities[i] != end and i not in path):
				if(current<i):
					first = current
					second = i-first
				else:
					first = i
					second = current-first
				if(cost>data[first][second]):
					best = i
					cost = data[first][second]
		path.append(best)
		current=best
		totalCost+=cost
		visited+=1

if __name__=='__main__':
	begin = 'Lisbon'
	end = 'Amsterdam'
	global bestPath_cost
	global bestPath_time
	global bestPath_distance
	global bestCost
	global bestTime
	global bestDistance
	

	data_cost=read_file('cost.csv')
	data_time=read_file('time.csv')	
	data_distance=read_file('distance.csv')
	cities=data_distance[0]
	data_cost=data_cost[1:]
	data_distance=data_distance[1:]
	data_time=data_time[1:]

	[bestPath_time,bestTime]=greedy(begin,end,data_time,cities)
	[bestPath_distance,bestDistance]=greedy(begin,end,data_distance,cities)
	[bestPath_cost,bestCost]=greedy(begin,end,data_cost,cities)
	

	hint=[]
	for i in range(len(bestPath_cost)):
		hint.append(bestPath_cost[i])

	
	path = [cities.index(begin)]
	i=1
	while(i<len(cities)-1):
		path.append(-1)
		i+=1
		
	path.append(cities.index(end))

	compute_route(cities,data_cost,data_time,data_distance,path,end,0,0,0,hint,1)

	portuguese = {'Lisbon':'Lisboa', 'Madrid':'Madrid', 'Bern':'Berna', 'Rome':'Roma', 'Athens':'Atenas', 'Vienna':'Viena', 'Prague':'Praga', 'Berlin':'Berlim', 'Copenhagen':'Copenhaga', 'Edinburgh':'Edimburgo', 'London':'Londres', 'Brussels':'Bruxelas', 'Paris':'Paris', 'Luxembourg':'Luxemburgo', 'Amsterdam':'Amesterdão'}

	s='A rota que mais económica começando em '+portuguese[begin]+' e terminando em '+portuguese[end]+' segue o percurso: '+portuguese[begin]+', '
	i=1
	while(i<len(cities)-1):
		s+=portuguese[cities[bestPath_cost[i]]]+', '
		i+=1
	s+=portuguese[end]+' custando um total de '+str(bestCost)+' euros'
	print(s)



	s='A rota que demora menos tempo começando em '+portuguese[begin]+' e terminando em '+portuguese[end]+' segue o percurso: '+portuguese[begin]+', '
	i=1
	while(i<len(cities)-1):
		s+=portuguese[cities[bestPath_time[i]]]+', '
		i+=1
	s+=portuguese[end]+' demorando um total de '+str(bestTime)+' horas'
	print(s)
	
	s='A rota que percorre menos distância começando em '+portuguese[begin]+' e terminando em '+portuguese[end]+' segue o percurso: '+portuguese[begin]+', '
	i=1
	while(i<len(cities)-1):
		s+=portuguese[cities[bestPath_distance[i]]]+', '
		i+=1
	s+=portuguese[end]+' percorrendo um total de '+str(bestDistance)+' km'
	print(s)





