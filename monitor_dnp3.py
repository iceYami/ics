alert tcp any any -> any 20000 (msg:"DNP3 DIRECT OPERATE"; content:"|05 64|"; depth:2; content:"|05|"; distance:0; within:1; sid:2000001;)
