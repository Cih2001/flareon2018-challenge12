def BreakPoint():
	bx = GetRegValue("bx")
	di = GetRegValue("di")
	ds = GetRegValue("ds")
	
	ba = bytearray(6)
	for i in range(6):
		ba[i] = Byte((ds << 4 ) + bx + di + i)
	hex_stream = " ".join(["%02X" % x for x in ba])
	
	ba = bytearray(16)
	for i in range(16):
		ba[i] = Byte((ds << 4 ) + di + i)
	data_stream = " ".join(["%02X" % x for x in ba])
	
	print ("%04X: %s data: %s" % (bx,hex_stream,data_stream))

	return False