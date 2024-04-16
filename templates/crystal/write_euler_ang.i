EULER_ANG_OUT[stress_out]
    # uses centroid
    type = ElementValueSampler
    variable = 'euler_angle_1 euler_angle_2 euler_angle_3'
    sort_by = 'id'
    # write to csv and exodus
    outputs = 'csv exodus'
    execute_on = TIMESTEP_END, FINAL
[]