

[AuxVariables]
    [stress_xx]
      family = MONOMIAL
      order = CONSTANT
    []
    [stress_yy]
      family = MONOMIAL
      order = CONSTANT
    []
    [stress_xy]
      family = MONOMIAL
      order = CONSTANT
    []
    [stress_zz]
      family = MONOMIAL
      order = CONSTANT
    []
    [stress_yz]
      family = MONOMIAL
      order = CONSTANT
    []
    [stress_xz]
      family = MONOMIAL
      order = CONSTANT
    []
    [strain_xx]
      family = MONOMIAL
      order = CONSTANT
    []
    [strain_yy]
      family = MONOMIAL
      order = CONSTANT
    []
    [strain_xy]
      family = MONOMIAL
      order = CONSTANT
    []
    [strain_zz]
      family = MONOMIAL
      order = CONSTANT
    []
    [strain_yz]
      family = MONOMIAL
      order = CONSTANT
    []
    [strain_xz]
      family = MONOMIAL
      order = CONSTANT
    []
[]

[AuxKernels]
    [stress_xx]
      type = RankTwoAux
      variable = stress_xx
      rank_two_tensor = pk1_stress
      index_i = 0
      index_j = 0
    []
    [stress_yy]
      type = RankTwoAux
      variable = stress_yy
      rank_two_tensor = pk1_stress
      index_i = 1
      index_j = 1
    []
    [stress_xy]
      type = RankTwoAux
      variable = stress_xy
      rank_two_tensor = pk1_stress
      index_i = 0
      index_j = 1
    []
  
    [stress_zz]
      type = RankTwoAux
      variable = stress_zz
      rank_two_tensor = pk1_stress
      index_i = 2
      index_j = 2
    []
    [stress_yz]
      type = RankTwoAux
      variable = stress_yz
      rank_two_tensor = pk1_stress
      index_i = 1
      index_j = 2
    []
    [stress_xz]
      type = RankTwoAux
      variable = stress_xz
      rank_two_tensor = pk1_stress
      index_i = 0
      index_j = 2
    []
  
    [strain_xx]
      type = RankTwoAux
      variable = strain_xx
      rank_two_tensor = mechanical_strain
      index_i = 0
      index_j = 0
    []
    [strain_yy]
      type = RankTwoAux
      variable = strain_yy
      rank_two_tensor = mechanical_strain
      index_i = 1
      index_j = 1
    []
    [strain_xy]
      type = RankTwoAux
      variable = strain_xy
      rank_two_tensor = mechanical_strain
      index_i = 0
      index_j = 1
    []
  
    [strain_zz]
      type = RankTwoAux
      variable = strain_zz
      rank_two_tensor = mechanical_strain
      index_i = 2
      index_j = 2
    []
    [strain_yz]
      type = RankTwoAux
      variable = strain_yz
      rank_two_tensor = mechanical_strain
      index_i = 1
      index_j = 2
    []
    [strain_xz]
      type = RankTwoAux
      variable = strain_xz
      rank_two_tensor = mechanical_strain
      index_i = 0
      index_j = 2
    []
  []