[Preconditioning]
	[smp]
	  type = SMP
	  full = false  
	[]
[]
  
[Executioner]
    type = Steady

    solve_type = 'pjfnk'
    line_search = 'bt'
    
    petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold'
    petsc_options_value = 'hypre     boomeramg      0.8'

    reuse_preconditioner = true
    reuse_preconditioner_max_linear_its = 10
  
    l_max_its = 100
    l_tol = 1e-12
    nl_max_its = 30
    nl_rel_tol = 1e-8
    nl_abs_tol = 1e-10

    automatic_scaling = true
    # scale contributions from each disp var and imposed strain independently
    scaling_group_variables = 'disp_x ; disp_y; disp_z; hvar'
[]