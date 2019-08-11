
def isStrong(s):
	a = False
	b = False
	c = False
	d = False
	for x in s:
		if x.isupper():
			a = True
		if x.islower():
			b = True
		if x.isdigit():
			c = True
		if len(s) >= 7:
			d = True
			
	
	if ((a==True) and (b==True) and (c==True) and (d==True)):
		return True
	else:
		return False
		
		

isStrong(input("enter"))