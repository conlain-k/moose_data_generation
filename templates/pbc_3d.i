
  [BCs]
	[Periodic]
	  [x]
			variable = disp_x
			auto_direction = 'x y z'
	  []
	  [y]
			variable = disp_y
			auto_direction = 'x y z'
	  []
	  [z]
			variable = disp_z
			auto_direction = 'x y z'
	  []
	[]

	[fix_origin_x]
		type = DirichletBC
		boundary = "origin"
		variable = disp_x
		value = 0
	[]

	[fix_origin_y]
		type = DirichletBC
		boundary = "origin"
		variable = disp_y
		value = 0
	[]

	[fix_origin_z]
		type = DirichletBC
		boundary = "origin"
		variable = disp_z
		value = 0
	[]
  
	[fix_x]
	  type = DirichletBC
	  boundary = "x_plus"
	  variable = disp_z
	  value = 0
	[]

	[fix_y]
	  type = DirichletBC
	  boundary = "y_plus"
	  variable = disp_x
	  value = 0
	[]

	[fix_z]
	  type = DirichletBC
	  boundary = "z_plus"
	  variable = disp_y
	  value = 0
	[]
[]