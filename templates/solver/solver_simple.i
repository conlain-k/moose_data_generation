# settings that worked well for buzzy

[Preconditioning]
  [smp]
    type = SMP
    full = false
  []
[]
 
[Executioner]
    type = Steady
    solve_type = "PJFNK"
 
    petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold'
    petsc_options_value = 'hypre     boomeramg      0.5'
 
    reuse_preconditioner = true
    reuse_preconditioner_max_linear_its = 10
 
    automatic_scaling = true
    scaling_group_variables = 'disp_x ; disp_y; disp_z'
 
[]