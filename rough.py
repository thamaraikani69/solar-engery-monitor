inv=1
smb=1
count=1
slave_id=0
for i in range(1,90):
	if i==39:
		smb+=1
		count+=1
		continue
	else:
		if count>13:
			inv+=1
			if inv==7:
				break
			smb=1
			ajb="ICR 1_INV "+str(inv)+"_SMB "+str(smb)+"_20 STRINGS"
			smb+=1
			count=2
		else:
			print(count)
			ajb="ICR 1_INV "+str(inv)+"_SMB "+str(smb)+"_20 STRINGS"
			smb+=1
			count+=1
	slave_id+=1
	print(ajb,slave_id)