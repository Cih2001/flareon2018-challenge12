from itertools import product

def compute_string_sum(str):
    result = 0
    for c in str:
        result += ord(c)
    return result
 
def compute_chars_sum(chr0, chr1, i):
    result =  ((ord(chr0)-0x20) + ((ord(chr1)-0x20)<<7)) & 0xffff
    result ^= ( i*33 ) & 0xffff
    return result
 
 
hashes = [0xFC7F,0xF30F,0xF361,0xF151,0xF886,0xF3D1,0xDB57,0xD9D5,0xE26E,0xF8CD,0xF969,0xD90C,0xF821,0xF181,0xF85F, 0xF883,0xE2A1,0xF47C,0xEA5B,0xFDFB]
tail = "@flare-on.com"
 
for i in range(40):
    head = "a"*i
    password = head + tail
    base = (((len(head) << 10) & 0xffff) + ((len(head) << 11) & 0xffff)) & 0xffff
   
    tails = [".com","n.co","on.c","-on.","e-on","re-o","are-","lare","flar","@fla","a@fl","aa@f","aaa@"]
    for t in tails:
        x = 13
        sum1 = hashes[x] - base - compute_chars_sum(t[0],t[1],x)
        sum2 = hashes[x+1] - base - compute_chars_sum(t[2],t[3],x+1)
        if sum1 == sum2:
            print (i, t, hex(sum1 & 0xffff))


password = head + tail

print(hex(hashes[13] - base - compute_chars_sum(".","c",13)))

def brute():

	head = "a"*(15)
	base = (((len(head) << 10) & 0xffff) + ((len(head) << 11) & 0xffff)) & 0xffff
	for i in range(20):
		for p in product('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwzyz0123456789_@.!#$%^&*()-/\|', repeat=2):
			if hashes[i] == base + compute_chars_sum(p[0],p[1],i) + 0x1d5e:
				print ("%s%s"%(p[0],p[1]), end = "")
			
			
	return True

brute()