[Preconditioning]
	[smp]
	  type = SMP
	  full = true
	[]
[]
  
[Executioner]
    type = Steady

    solve_type = 'newton'
    line_search = none

    petsc_options_iname = '-pc_type'
    petsc_options_value = 'lu'

    l_max_its = 2
    l_tol = 1e-14
    nl_max_its = 30
    nl_rel_tol = 1e-8
    nl_abs_tol = 1e-10
[]