[Preconditioning]
	[smp]
	  type = SMP
	  full = true  
	[]
[]
  
[Executioner]
    type = Steady

    solve_type = 'newton'
    petsc_options = '-pc_svd_monitor'
    petsc_options_iname = '-pc_type'
    petsc_options_value = 'svd'
[]