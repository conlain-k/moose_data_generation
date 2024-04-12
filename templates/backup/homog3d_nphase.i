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
		output=true

		subdomain_ids = {{subdomain_ids}}
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
		     	# xx xy xz yx yy yz zx zy zz for large strain
				# TODO check large strain equivalent
				constraint_types = 'strain strain strain none strain strain none none strain'
				targets = 'bc_strain_xx bc_strain_xy bc_strain_xz bc_strain_yy bc_strain_yz bc_strain_zz '
				generate_output = 'cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz cauchy_stress_xy cauchy_stress_xz cauchy_stress_yz strain_xx strain_yy strain_zz strain_xy strain_xz strain_yz'
			[]
		[]
	[]
[]	


[Functions]
	[bc_strain_xx]
		type = ParsedFunction
		expression = '{{STRAIN_XX}}'
	[]
	[bc_strain_yy]
		type = ParsedFunction
		expression = '{{STRAIN_YY}}'
	[]
	[bc_strain_zz]
		type = ParsedFunction
		expression = '{{STRAIN_ZZ}}'
	[]
	[bc_strain_yz]
		type = ParsedFunction
		expression = '{{STRAIN_YZ}}'
	[]
	[bc_strain_xz]
		type = ParsedFunction
		expression = '{{STRAIN_XZ}}'
	[]
	[bc_strain_xy]
		type = ParsedFunction
		expression = '{{STRAIN_XY}}'
	[]
	[zero]
		type = ParsedFunction
		expression = '0'
	[]
[]

# [ICs]
# []

# Periodic Boundary conditions
!include templates/pbc_3d.i

[Materials]
{{ELAST_TENSORS}}

[compute_stress]
	type = ComputeLagrangianLinearElasticStress
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
		variable = 'cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz cauchy_stress_xy cauchy_stress_xz cauchy_stress_yz'
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
