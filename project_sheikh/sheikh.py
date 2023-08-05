counter = 0

def num_to_str(num):
    return(str(bin(num))[2:].rjust(8, '0'))

for wife1 in range(256):
    for wife2 in range(256):
        for wife3 in range(256):

            w1_lst = num_to_str(wife1)
            w2_lst = num_to_str(wife2)
            w3_lst = num_to_str(wife3)
            
            cur_jewel = 0
            
            for jewel in range(8):
                if ((w1_lst[jewel] == '0') or \
                    ((w1_lst[jewel] == '1') and (w2_lst[jewel] == '0') and (w3_lst[jewel] == '0'))) and \
                    ((w3_lst[jewel] == '0') or ((w2_lst[jewel] == '1') and (w3_lst[jewel] == '1'))):
                        cur_jewel += 1
            if cur_jewel == 8:
                counter += 1

print(counter)
    


    

