alert tcp any any -> any 20000 (msg:"DNP3 COLD RESTART"; content:"|0D|"; offset:10; depth:1; sid:2000002;)
