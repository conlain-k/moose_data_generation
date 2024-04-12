[elastic_tensor]
	type = ComputeElasticityTensorCP
	C_ijkl = '{{C11}} {{C12}} {{C12}} {{C11}} {{C12}} {{C11}} {{C44}} {{C44}} {{C44}}' 
	fill_method = symmetric9
	read_prop_user_object = prop_read
[]
