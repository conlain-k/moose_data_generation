[Preconditioning]
	[smp]
	  type = SMP
	  full = false  
	[]
[]
  
[Executioner]
    type = Steady

    # solve_type = 'pjfnk'
    # line_search = noneions_iname = '-ksp_type -pc_type '
    # petsc_options_value = 'KSPGMRES, bjacobi'


    # petsc_options_iname = '-pc_type'
    # petsc_options_value = 'lu'
    
    petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold'
    petsc_options_value = 'hypre     boomeramg      0.7'


    # petsc_options_iname = '-pc_type -pc_asm_overlap -sub_pc_type -ksp_type -ksp_gmres_restart'
    # petsc_options_value = ' asm      2              lu            gmres     200'

    # petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold -pc_hypre_boomeramg_interp_type -pc_hypre_boomeramg_coarsen_type'
    # petsc_options_value = 'hypre     boomeramg      0.4 ext+i HMIS'

    # petsc_options_iname = '-ksp_type -pc_type '
    # petsc_options_value = 'KSPGMRES, bjacobi'

    # petsc_options = '-snes_converged_reason'
    # petsc_options_iname = '-ksp_type -pc_type -sub_pc_type -snes_max_it -sub_pc_factor_shift_type -pc_asm_overlap -snes_atol -snes_rtol '
    # petsc_options_value = 'gmres asm lu 100 NONZERO 2 1E-14 1E-12'

    reuse_preconditioner = true
    reuse_preconditioner_max_linear_its = 10
  
    l_max_its = 20
    l_tol = 1e-6
    nl_max_its = 30
    nl_rel_tol = 1e-8
    nl_abs_tol = 1e-10

    automatic_scaling = true
    scaling_group_variables = 'disp_x ; disp_y; disp_z'
[]