x 		= [1,1,2,2,2,5,5,5,5,7,7,7,7,9,9,9,9,10,10,10,10,10,10]
comp 	= [0,3,4,5,6,7,8,9]

vector 	= [0] *(len(comp) -1)
count_i = 0; count_j = 1;

for each in x:
	if(each < comp[count_j]):
		pass		
	else:
		while(each >= comp[count_j]):
			if(count_j >= len(comp) -1):
				break
			else:
				count_i 	+= 1
				count_j 	+= 1
	vector[count_i] += 1					

print(vector)