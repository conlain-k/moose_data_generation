# 2D with mixed conditions on stress/strain

[GlobalParams]
	displacements = 'disp_x disp_y disp_z'
#	C11 = 160
#	C12 = 70
#	C44 = 60
[]

[Mesh]
	[generated]
	  type = GeneratedMeshGenerator
	  dim = 3
	  nx = 62
	  ny = 62
	  nz = 62
	  xmax = 1
	  ymax = 1
	  zmax = 1
	  elem_type = HEX8
	  show_info=true
	[]
	
	[origin_set]
		type=ExtraNodesetGenerator
		new_boundary = "origin"
		coord = "0 0 0"
		input=generated
	[]

	[xp_set]
		type=ExtraNodesetGenerator
		new_boundary = "x_plus"
		coord = "1 0 0"
		input=origin_set
	[]
	[yp_set]
		type=ExtraNodesetGenerator
		new_boundary = "y_plus"
		coord = "0 1 0"
		input=xp_set
	[]
	[zp_set]
		type=ExtraNodesetGenerator
		new_boundary = "z_plus"
		coord = "0 0 1"
		input=yp_set
	[]
[]

[UserObjects]
  [./prop_read]
    type = PropertyReadFile
    prop_file_name = 'poly.txt'
    nprop = 3
    read_type = element
  [../]
[]

# pull in aux var definitions

[Physics]
	[SolidMechanics]
	  [QuasiStatic]
		[all]
		  strain = SMALL
		#verbose=true
		  add_variables = true
		  new_system = true
		  formulation = TOTAL
		  volumetric_locking_correction = false
		  constraint_types = 'strain strain strain none strain strain none none strain'
			targets = 'strain_001 zero zero zero zero zero zero zero zero'
		generate_output = 'cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz cauchy_stress_xy cauchy_stress_xz cauchy_stress_yz strain_xx strain_yy strain_zz strain_xy strain_xz strain_yz'
		[]
	  []
	[]
[]
  
[Functions]
  [strain_001]
    type = ParsedFunction
    expression = '0.001'
  []
	[zero]
    type = ParsedFunction
    expression = '0'
  []
[]

# Periodic Boundary conditions
!include templates/pbc_3d.i

  
[Materials]
	#[./strain]
	#	type = ComputeFiniteStrain
	#	displacements = 'disp_x disp_y disp_z'
	#[../]
	[./elasticity_tensor]
		type = ComputeElasticityTensorCP
		C_ijkl = '160 70 70 160 70 160 60 60 60' 
		#C_ijkl = '${C11} ${C12} ${C12} ${C11} ${C12} ${C11} ${C44} ${C44} ${C44}' 
		fill_method = symmetric9
		read_prop_user_object = prop_read
	[../]
	[compute_stress]
		type = ComputeLagrangianLinearElasticStress
	[]
[]
  
!include templates/solver.i


[VectorPostprocessors]
	[strain_out]
	  type = ElementValueSampler
	  variable = 'strain_xx strain_xy strain_yy'
	  sort_by = 'id'
	  outputs = csv
	  execute_on = TIMESTEP_END
	[]
  []
  
  [Outputs]
	[csv]
		type = CSV
		#file_base = "poly"
	[]
	exodus=true
	print_linear_residuals = true
  []
  