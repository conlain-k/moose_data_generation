# 2D with mixed conditions on stress/strain

[GlobalParams]
	displacements = 'u_x u_y u_z'
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
		output=true

		subdomain_ids = {{subdomain_ids}}
	[]

	[origin_set]
		type=ExtraNodesetGenerator
		new_boundary = "origin"
		coord = "0.5 0.5 0.5"
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

[Variables]
	[global_strain_var]
		order = SIXTH
		family = SCALAR
	[]
[]

[AuxVariables]
	[./disp_x]
	[]
	[./disp_y]
	[]
	[./disp_z]
	[]
[]

[ICs]
	[./InitialCondition]
		type = ConstantIC
		value = 1
		variable = u_x
	[]
[]

[AuxKernels]
	[./disp_x]
	  type = GlobalDisplacementAux
	  variable = disp_x
	  scalar_global_strain = global_strain_var
	  global_strain_uo = global_strain_uo
	  component = 1
	[]
	[./disp_y]
	  type = GlobalDisplacementAux
	  variable = disp_y
	  scalar_global_strain = global_strain_var
	  global_strain_uo = global_strain_uo
	  component = 1
	[]
	[./disp_z]
	  type = GlobalDisplacementAux
	  variable = disp_z
	  scalar_global_strain = global_strain_var
	  global_strain_uo = global_strain_uo
	  component = 2
	[]
[]

[ScalarKernels]
	[global_strain]
	  type = GlobalStrain
	  variable = global_strain_var
	  global_strain_uo = global_strain_uo
	[]
[]
  

[Physics]
	[SolidMechanics]
		[QuasiStatic]
			[all]
				strain = SMALL
				verbose=true
				add_variables = true
				# global strain contribution
				global_strain = global_strain
				
				# displacements= 'u_x u_y u_z'
		     	# xx xy xz yx yy yz zx zy zz for large strain
				# TODO check large strain equivalent
				# constraint_types = 'strain strain strain none strain strain none none strain'
				# targets = 'bc_strain_xx bc_sturain_xy bc_strain_xz bc_strain_yy bc_strain_yz bc_strain_zz '
				generate_output = 'stress_xx stress_yy stress_zz stress_xy stress_xz stress_yz strain_xx strain_yy strain_zz strain_xy strain_xz strain_yz'
			[]
		[]
	[]
[]	

[UserObjects]
	[./global_strain_uo]
	  type = GlobalStrainUserObject
	#   applied_stress_tensor = '10 10 10 0 0 0'
	  execute_on = 'Initial Linear Nonlinear'
	[]
[]

# Periodic Boundary conditions
!include templates/pbc_3d.i

[Materials]
{{ELAST_TENSORS}}

[compute_stress]
	type = ComputeLinearElasticStress
[]

[compute_global_strain]
    type = ComputeGlobalStrain
    scalar_global_strain = global_strain_var
    global_strain_uo = global_strain_uo
[]

[]

# !include templates/solver_debug.i
!include templates/solver.i



[VectorPostprocessors]
	[strain_out]
		type = ElementValueSampler
		variable = 'strain_xx strain_yy strain_zz strain_xy strain_xz strain_yz'
		sort_by = 'id'
		outputs = csv
		execute_on = TIMESTEP_END
	[]
	[stress_out]
		type = ElementValueSampler
		variable = 'stress_xx stress_yy stress_zz stress_xy stress_xz stress_yz'
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

print_perf_log = true
exodus = true
# show_var_residual_norms = true

[]
