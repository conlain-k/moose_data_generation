# 2D with mixed conditions on stress/strain

[GlobalParams]
	displacements = 'disp_x disp_y disp_z'
[]

[Mesh]
	[generated]
	  type = GeneratedMeshGenerator
	  dim = 3
	  nx = {{N_x}}
	  ny = {{N_y}}
	  nz = {{N_z}}
	  xmax = 1
	  ymax = 1
	  zmax = 1
	  elem_type = HEX8
	  show_info=true
	[]
	
	[subdomain_id]
	  type = SubdomainPerElementGenerator
	  subdomain_ids = {{subdomain_ids}}
	  input = generated
	[]

	[origin_set]
		type=ExtraNodesetGenerator
		new_boundary = "origin"
		coord = "0 0 0"
		input=subdomain_id
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

# pull in aux var definitions
# !include templates/auxvars.i

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
[elastic_tensor_1]
	type = ComputeIsotropicElasticityTensor
	youngs_modulus = 120
	poissons_ratio = 0.3
	block = '0'
[]
# [elastic_tensor_2]
# 	type = ComputeIsotropicElasticityTensor
# 	youngs_modulus = 120000
# 	poissons_ratio = 0.3
# 	block = '1'
# []
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
		file_base = "{{OUTPUT_DIR}}/{{base_name}}"
	[]
  []
  