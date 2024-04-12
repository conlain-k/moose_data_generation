# 2D with mixed conditions on stress/strain

[GlobalParams]
	displacements = 'disp_x disp_y disp_z'
	# change for finite-strain
	large_kinematics = false
	# DO NOT DISABLE THIS!!! required for same results as abaqus
	stabilize_strain = true

	# these two are used for periodic BCs
	macro_gradient = hvar
	homogenization_constraint = homogenization
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

		# only used for n-phase structures
		{{subdomain_info}}	
	[]

	# set some node sets for periodic BCs
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

[Variables]
	# set up displacement vars
	[disp_x]
	[]
	[disp_y]
	[]
	[disp_z]
	[]
	# used for periodic BCs
	[hvar]
	  family = SCALAR
	  order = SIXTH
	[]
[]


# TODO figure out what a good initial guess is
[ICs]
	[./xinit_0]
		type = RandomIC
		min = 0
		max = "{{DISP_X_INIT}}"
		variable = disp_x
	[]
	[./yinit]
		type = RandomIC
		min = 0
		max = "{{DISP_Y_INIT}}"
		variable = disp_y
	[]
	[./zinit]
		type = RandomIC
		min = 0
		max = "{{DISP_Z_INIT}}"
		variable = disp_z
	[]
[]


# no need to change this, it just enforces PBCs
[UserObjects]
	[homogenization]
		type = HomogenizationConstraint
		# xx xy xz yx yy yz zx zy zz 
		constraint_types = 'strain strain strain none strain strain none none strain'
		targets = 'bc_strain_xx bc_strain_xy bc_strain_xz bc_strain_yy bc_strain_yz bc_strain_zz '
		execute_on = 'INITIAL LINEAR NONLINEAR'
	[]

	# add crystal file info (only for crystalline)
	{{CRYSTAL_FILE_INFO}}
[]

# set average strain values for BCs
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


# enforce PBC
[ScalarKernels]
	[enforce]
	  type = HomogenizationConstraintScalarKernel
	  variable = hvar
	[]
[]
  
# these enforce the actual physics (div sigma = 0)
[Kernels]
	[sdx]
		type = HomogenizedTotalLagrangianStressDivergence
		variable = disp_x
		component = 0
	[]
	[sdy]
		type = HomogenizedTotalLagrangianStressDivergence
		variable = disp_y
		component = 1
	[]
	[sdz]
		type = HomogenizedTotalLagrangianStressDivergence
		variable = disp_z
		component = 2
	[]
[]

# defines variables for postprocessing
!include templates/auxvars.i

# Periodic boundary conditions (dirichlet, etc.)
!include templates/pbc_3d.i

# set up material properties and outputs
[Materials]
	# used for either crystal or 2phase
	{{ELAST_TENSORS}}

	[compute_stress]
		type = ComputeLagrangianLinearElasticStress
	[]

	[compute_strain]
		type = ComputeLagrangianStrain
		homogenization_gradient_names = 'homogenization_gradient'
	[]

	[compute_homogenization_gradient]
		type = ComputeHomogenizedLagrangianStrain
	[]

[]

# solver settings
!include templates/solver.i
# !include templates/solver_debug.i

# outputs for CSV file
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
