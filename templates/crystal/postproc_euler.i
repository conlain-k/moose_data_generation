[euler_ang]
    type=ElementValueSampler
    # variable="Euler_angles_x Euler_angles_y Euler_angles_z elasticity_tensor_0000 elasticity_tensor_1111 elasticity_tensor_0011 elasticity_tensor_2222 elasticity_tensor_0101 elasticity_tensor_1212" 
    variable="elasticity_tensor_0000 elasticity_tensor_1111 elasticity_tensor_0011 elasticity_tensor_2222 elasticity_tensor_0101 elasticity_tensor_1212" 
    sort_by = id
    outputs = csv
[]