# 2D with mixed conditions on stress/strain

[GlobalParams]
	displacements = 'disp_x disp_y'
[]

[Mesh]
	[generated]
	  type = GeneratedMeshGenerator
	  dim = 2
	  nx = {{N_x}}
	  ny = {{N_x}}
	  xmax = 1
	  ymax = 1
	  elem_type = QUAD4
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
		coord = "0 0"
		input=subdomain_id
	[]

	[xp_set]
		type=ExtraNodesetGenerator
		new_boundary = "x_plus"
		coord = "1 0"
		input=origin_set
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
		#   new_system = true
		#   formulation = TOTAL
		  volumetric_locking_correction = false
		#   constraint_types = 'strain strain strain none none none none none none'
			# targets = 'strain_001 zero zero'
			generate_output = 'stress_xx stress_yy stress_zz stress_xy stress_xz stress_yz strain_xx strain_yy strain_zz strain_xy strain_xz strain_yz'
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
!include templates/pbc_2d.i
  
[Materials]
[elastic_tensor_1]
	type = ComputeIsotropicElasticityTensor
	youngs_modulus = {{E0}}
	poissons_ratio = 0.3
	block = '0'
[]
[elastic_tensor_2]
	type = ComputeIsotropicElasticityTensor
	youngs_modulus = {{E1}}
	poissons_ratio = 0.3
	block = '1'
[]
[compute_stress]
	type = ComputeLinearElasticStress
[]
[]
  
!include templates/solver_debug.i
#!include templates/solver.i

[ICs]
	[init_x]
		type = ConstantIC
		value = 0.5
		variable = 'disp_x'
	[]
	[init_y]
		type = ConstantIC
		value = 0.5
		variable = 'disp_y'
	[]
[]


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
  