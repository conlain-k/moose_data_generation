# these settings scream for crystal structures specifically (less linear calls)
[Preconditioning]
	[smp]
	  type = SMP
	  full = false  
	[]
[]
  
[Executioner]
    type = Steady

    # preconditioned jacobian-free newton krylov
    solve_type = 'pjfnk'
    # no line search since our homog. system is nearly linear (jacobian should be pretty stable)
    line_search = 'bt'
    
    # Print out reason for convergence
    petsc_options = '-snes_converged_reason'
    
    # Put petsc options here 
    # petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold -ksp_type'
    # petsc_options_value = 'hypre     boomeramg      0.65 bcgs'
    
    
    # petsc_options =       '-snes_converged_reason -ksp_gmres_modifiedgramschmidt'
    # petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold -ksp_gmres_restart'
    # petsc_options_value = 'hypre     boomeramg      0.4 20'


    # keep approx jacobian between NL iters (since it shouldn't change much)
    reuse_preconditioner = true
    reuse_preconditioner_max_linear_its = 10

    

    # small linear tolerance, allow NL tol to control convergence
    l_tol = 1e-2
    # Relative to initial guess = keep small
    nl_rel_tol = 1e-12
    # Absolute acceptable error in div sigma
    nl_abs_tol = 1e-9

    # this helps conditioning a lot
    automatic_scaling = true
    # scale contributions from each disp var and imposed strain independently
    scaling_group_variables = 'disp_x ; disp_y; disp_z; hvar'
[]
