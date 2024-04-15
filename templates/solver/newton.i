[Preconditioning]
	[smp]
	  type = SMP
          # make sure to build the full jacobian
	  full = true  
	[]
[]
  
[Executioner]
    type = Steady
    # just use Newton's method with full jacobian, direct solver
    solve_type = 'newton'
    petsc_options_iname = '-pc_type'
    petsc_options_value = 'lu'
[]
