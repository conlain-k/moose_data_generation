
  [BCs]
	[Periodic]
	  [x]
		variable = disp_x
		auto_direction = 'x y'
	  []
	  [y]
		variable = disp_y
		auto_direction = 'x y'
	  []
	[]
  
	[fix1_x]
	  type = DirichletBC
	  boundary = "origin"
	  variable = disp_x
	  value = 0
	[]
	[fix1_y]
	  type = DirichletBC
	  boundary = "origin"
	  variable = disp_y
	  value = 0
	[]
  
	[fix2_y]
	  type = DirichletBC
	  boundary = "x_plus"
	  variable = disp_y
	  value = 0
	[]
  []