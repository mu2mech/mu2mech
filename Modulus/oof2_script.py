def step1(data):
    oof2_script_str = f"OOF.Windows.Graphics.New()  \n" \
        f"OOF.Graphics_1.Settings.New_Layer_Policy(policy='Single') \n" \
        f"OOF.Microstructure.Create_From_ImageFile(filename='{data['output_path']}/{data['image_name']}', microstructure_name='{data['image_name']}', height=automatic, width=automatic) \n" \
        f"OOF.PixelGroup.New(name='phase_1', microstructure='{data['image_name']}') \n" \
        f"OOF.PixelGroup.New(name='phase_2', microstructure='{data['image_name']}') \n" \
        f"OOF.Graphics_1.Toolbox.Pixel_Select.Burn(source='{data['image_name']}:{data['image_name']}', local_flammability=0.1, global_flammability=0.2, color_space_norm='L1', next_nearest=False, points=[Point({data['coordinate']['x']},{data['coordinate']['y']})], shift=0, ctrl=0) \n" \
        f"OOF.PixelGroup.AddSelection(microstructure='{data['image_name']}', group='phase_1') \n" \
        f"OOF.Graphics_1.Toolbox.Pixel_Select.Invert(source='{data['image_name']}:{data['image_name']}') \n" \
        f"OOF.PixelGroup.AddSelection(microstructure='{data['image_name']}', group='phase_2') \n" \
        f"OOF.Material.New(name='phase_1_1000k', material_type='bulk') \n" \
        f"OOF.Material.New(name='phase_2_1000k', material_type='bulk') \n" \
        f"OOF.Property.Copy(property='Mechanical:Elasticity:Anisotropic:Cubic', new_name='phase_1') \n" \
        f"OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.phase_1(cijkl=CubicRank4TensorCij(c11={data['elastic_constants']['phase_1']['C11']},c12={data['elastic_constants']['phase_1']['C12']},c44={data['elastic_constants']['phase_1']['C44']})) \n" \
        f"OOF.Property.Copy(property='Orientation', new_name='phase_1') \n" \
        f"OOF.Property.Parametrize.Orientation.phase_1(angles=XYZ(phi=0,theta=0,psi=0)) \n" \
        f"OOF.Material.Add_property(name='phase_1_1000k', property='Orientation:phase_1') \n" \
        f"OOF.Material.Add_property(name='phase_1_1000k', property='Mechanical:Elasticity:Anisotropic:Cubic:phase_1') \n" \
        f"OOF.Property.Copy(property='Mechanical:Elasticity:Anisotropic:Cubic', new_name='phase_2') \n" \
        f"OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.phase_2(cijkl=CubicRank4TensorCij(c11={data['elastic_constants']['phase_2']['C11']},c12={data['elastic_constants']['phase_2']['C12']},c44={data['elastic_constants']['phase_2']['C44']})) \n" \
        f"OOF.Property.Copy(property='Orientation', new_name='phase_2') \n" \
        f"OOF.Property.Parametrize.Orientation.phase_2(angles=XYZ(phi=0,theta=0,psi=0)) \n" \
        f"OOF.Material.Add_property(name='phase_2_1000k', property='Orientation:phase_2') \n" \
        f"OOF.Material.Add_property(name='phase_2_1000k', property='Mechanical:Elasticity:Anisotropic:Cubic:phase_2') \n" \
        f"OOF.Material.Assign(material='phase_2_1000k', microstructure='{data['image_name']}', pixels='phase_2') \n" \
        f"OOF.Material.Assign(material='phase_1_1000k', microstructure='{data['image_name']}', pixels='phase_1') \n" \
        f"OOF.Skeleton.New(name='skeleton', microstructure='{data['image_name']}', x_elements={data['mesh']['x_elements']}, y_elements={data['mesh']['y_elements']}, skeleton_geometry=QuadSkeleton(left_right_periodicity=True,top_bottom_periodicity=True)) \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9) \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Refine(targets=CheckSelectedElements(),criterion=Unconditionally(),degree=Trisection(rule_set='conservative'),alpha=0.5)) \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9) \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=SnapNodes(targets=SnapSelected(),criterion=AverageEnergy(alpha=0.5))) \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9) \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Anneal(targets=FiddleSelectedElements(),criterion=AverageEnergy(alpha=0.5),T=0.0,delta=1.0,iteration=FixedIteration(iterations=5))) \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Rationalize(targets=AllElements(),criterion=AverageEnergy(alpha=0.5),method=SpecificRationalization(rationalizers=[RemoveShortSide(ratio=5.0), QuadSplit(angle=150), RemoveBadTriangle(acute_angle=15,obtuse_angle=150)]))) \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=FixIllegal()) \n" \
        f"OOF.Mesh.New(name='mesh', skeleton='{data['image_name']}:skeleton', element_types=['D2_2', 'T3_3', 'Q4_4']) \n" \
        f"OOF.Subproblem.Field.Define(subproblem='{data['image_name']}:skeleton:mesh:default', field=Displacement) \n" \
        f"OOF.Subproblem.Field.Activate(subproblem='{data['image_name']}:skeleton:mesh:default', field=Displacement) \n" \
        f"OOF.Subproblem.Equation.Activate(subproblem='{data['image_name']}:skeleton:mesh:default', equation=Force_Balance) \n" \
        f"OOF.Subproblem.Equation.Activate(subproblem='{data['image_name']}:skeleton:mesh:default', equation=Plane_Stress) \n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc1', mesh='{data['image_name']}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='x',equation=Force_Balance,eqn_component='x',profile=ConstantProfile(value={data['boundary_conditions']['bc1']['value']}),boundary='{data['boundary_conditions']['bc1']['boundary']}')) \n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc2', mesh='{data['image_name']}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='x',equation=Force_Balance,eqn_component='x',profile=ConstantProfile(value={data['boundary_conditions']['bc2']['value']}),boundary='{data['boundary_conditions']['bc2']['boundary']}')) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('GraphicsUpdate'), output=GraphicsUpdate()) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('GraphicsUpdate'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Stress[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Flux:Component',component='xx',flux=Stress),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic))) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[xx]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn1_stress_xx ',mode='w')) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Stress[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Flux:Component',component='yy',flux=Stress),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic))) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[yy]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn1_stress_yy ',mode='w')) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Geometric Strain[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='xx',type=GeometricStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic))) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[xx]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn1_geom_strain_xx',mode='w')) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Geometric Strain[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='yy',type=GeometricStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic))) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[yy]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn1_geom_strain_yy',mode='w')) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Elastic Strain[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='xx',type=ElasticStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic))) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[xx]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn1_elastic_strain_xx',mode='w')) \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Elastic Strain[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='yy',type=ElasticStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic))) \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0)) \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[yy]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn1_elastic_strain_yy',mode='w')) \n" \
        f"OOF.File.Save.Mesh(filename='{data['output_path']}/40_1000K_t2_512_x_dir_mesh_abaqus', mode='w', format='abaqus', mesh='{data['image_name']}:skeleton:mesh') \n" \
        f"OOF.Subproblem.Set_Solver(subproblem='{data['image_name']}:skeleton:mesh:default', solver_mode=BasicSolverMode(time_stepper=BasicStaticDriver(),matrix_method=BasicIterative(tolerance=1e-13,max_iterations=10000))) \n" \
        f"OOF.Mesh.Set_Field_Initializer(mesh='{data['image_name']}:skeleton:mesh', field=Displacement, initializer=ConstTwoVectorFieldInit(cx=0.0,cy=0.0)) \n" \
        f"OOF.Mesh.Apply_Field_Initializers(mesh='{data['image_name']}:skeleton:mesh') \n" \
        f"OOF.Mesh.Solve(mesh='{data['image_name']}:skeleton:mesh', endtime=0.0) \n" \
        f"exit()"

    f = open("OOF2/temp_scripts/script", "w")
    f.write(oof2_script_str)
    f.close()


def step2(data):
    oof2_script_str = f"OOF.Windows.Graphics.New()  \n" \
        f"OOF.Graphics_1.Settings.New_Layer_Policy(policy='Single') \n" \
        f"OOF.Microstructure.Create_From_ImageFile(filename='{data['output_path']}/{data['image_name']}', microstructure_name='{data['image_name']}', height=automatic, width=automatic) \n" \
        f"OOF.PixelGroup.New(name='phase_1', microstructure='{data['image_name']}')  \n" \
        f"OOF.PixelGroup.New(name='phase_2', microstructure='{data['image_name']}')  \n" \
        f"OOF.Graphics_1.Toolbox.Pixel_Select.Burn(source='{data['image_name']}:{data['image_name']}', local_flammability=0.1, global_flammability=0.2, color_space_norm='L1', next_nearest=False, points=[Point({data['coordinate']['x']},{data['coordinate']['y']})], shift=0, ctrl=0)  \n" \
        f"OOF.PixelGroup.AddSelection(microstructure='{data['image_name']}', group='phase_1')  \n" \
        f"OOF.Graphics_1.Toolbox.Pixel_Select.Invert(source='{data['image_name']}:{data['image_name']}')  \n" \
        f"OOF.PixelGroup.AddSelection(microstructure='{data['image_name']}', group='phase_2')  \n" \
        f"OOF.Material.New(name='phase_1_1000k', material_type='bulk')  \n" \
        f"OOF.Material.New(name='phase_2_1000k', material_type='bulk')  \n" \
        f"OOF.Property.Copy(property='Mechanical:Elasticity:Anisotropic:Cubic', new_name='phase_1')  \n" \
        f"OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.phase_1(cijkl=CubicRank4TensorCij(c11={data['elastic_constants']['phase_1']['C11']},c12={data['elastic_constants']['phase_1']['C12']},c44={data['elastic_constants']['phase_1']['C44']}))  \n" \
        f"OOF.Property.Copy(property='Orientation', new_name='phase_1')  \n" \
        f"OOF.Property.Parametrize.Orientation.phase_1(angles=XYZ(phi=0,theta=0,psi=0))  \n" \
        f"OOF.Material.Add_property(name='phase_1_1000k', property='Orientation:phase_1')  \n" \
        f"OOF.Material.Add_property(name='phase_1_1000k', property='Mechanical:Elasticity:Anisotropic:Cubic:phase_1')  \n" \
        f"OOF.Property.Copy(property='Mechanical:Elasticity:Anisotropic:Cubic', new_name='phase_2')  \n" \
        f"OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.phase_2(cijkl=CubicRank4TensorCij(c11={data['elastic_constants']['phase_2']['C11']},c12={data['elastic_constants']['phase_2']['C12']},c44={data['elastic_constants']['phase_2']['C44']}))  \n" \
        f"OOF.Property.Copy(property='Orientation', new_name='phase_2')  \n" \
        f"OOF.Property.Parametrize.Orientation.phase_2(angles=XYZ(phi=0,theta=0,psi=0))  \n" \
        f"OOF.Material.Add_property(name='phase_2_1000k', property='Orientation:phase_2')  \n" \
        f"OOF.Material.Add_property(name='phase_2_1000k', property='Mechanical:Elasticity:Anisotropic:Cubic:phase_2')  \n" \
        f"OOF.Material.Assign(material='phase_2_1000k', microstructure='{data['image_name']}', pixels='phase_2')  \n" \
        f"OOF.Material.Assign(material='phase_1_1000k', microstructure='{data['image_name']}', pixels='phase_1')  \n" \
        f"OOF.Skeleton.New(name='skeleton', microstructure='{data['image_name']}', x_elements={data['mesh']['x_elements']}, y_elements={data['mesh']['y_elements']}, skeleton_geometry=QuadSkeleton(left_right_periodicity=True,top_bottom_periodicity=True))  \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9)  \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Refine(targets=CheckSelectedElements(),criterion=Unconditionally(),degree=Trisection(rule_set='conservative'),alpha=0.5))  \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9)  \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Refine(targets=CheckSelectedElements(),criterion=Unconditionally(),degree=Trisection(rule_set='conservative'),alpha=0.5))  \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9)  \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=SnapNodes(targets=SnapSelected(),criterion=AverageEnergy(alpha=0.5)))  \n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{data['image_name']}:skeleton', threshold=0.9)  \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Anneal(targets=FiddleSelectedElements(),criterion=AverageEnergy(alpha=0.5),T=0.0,delta=1.0,iteration=FixedIteration(iterations=5)))  \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=Rationalize(targets=AllElements(),criterion=AverageEnergy(alpha=0.5),method=SpecificRationalization(rationalizers=[RemoveShortSide(ratio=5.0), QuadSplit(angle=150), RemoveBadTriangle(acute_angle=15,obtuse_angle=150)])))  \n" \
        f"OOF.Skeleton.Modify(skeleton='{data['image_name']}:skeleton', modifier=FixIllegal())  \n" \
        f"OOF.Mesh.New(name='mesh', skeleton='{data['image_name']}:skeleton', element_types=['D2_2', 'T3_3', 'Q4_4'])  \n" \
        f"OOF.Subproblem.Field.Define(subproblem='{data['image_name']}:skeleton:mesh:default', field=Displacement)  \n" \
        f"OOF.Subproblem.Field.Activate(subproblem='{data['image_name']}:skeleton:mesh:default', field=Displacement)  \n" \
        f"OOF.Subproblem.Equation.Activate(subproblem='{data['image_name']}:skeleton:mesh:default', equation=Force_Balance)  \n" \
        f"OOF.Subproblem.Equation.Activate(subproblem='{data['image_name']}:skeleton:mesh:default', equation=Plane_Stress)  \n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc1', mesh='{data['image_name']}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='x',equation=Force_Balance,eqn_component='x',profile=ConstantProfile(value={data['boundary_conditions']['bc1']['value']}),boundary='{data['boundary_conditions']['bc1']['boundary']}'))  \n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc2', mesh='{data['image_name']}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='x',equation=Force_Balance,eqn_component='x',profile=ConstantProfile(value={data['boundary_conditions']['bc2']['value']}),boundary='{data['boundary_conditions']['bc2']['boundary']}'))  \n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc3', mesh='{data['image_name']}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='y',equation=Force_Balance,eqn_component='y',profile=ConstantProfile(value={(data['p_ratio'])*float(data['boundary_conditions']['bc1']['value'])}),boundary='top'))  \n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc4', mesh='{data['image_name']}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='y',equation=Force_Balance,eqn_component='y',profile=ConstantProfile(value={data['p_ratio']*float(data['boundary_conditions']['bc2']['value'])}),boundary='bottom'))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('GraphicsUpdate'), output=GraphicsUpdate())  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('GraphicsUpdate'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Stress[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Flux:Component',component='xx',flux=Stress),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[xx]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn2_stress_xx ',mode='w'))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Stress[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Flux:Component',component='yy',flux=Stress),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Stress[yy]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn2_stress_yy ',mode='w'))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Geometric Strain[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='xx',type=GeometricStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[xx]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn2_geom_strain_xx',mode='w'))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Geometric Strain[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='yy',type=GeometricStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Geometric Strain[yy]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn2_geom_strain_yy',mode='w'))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Elastic Strain[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='xx',type=ElasticStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[xx]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn2_elastic_strain_xx',mode='w'))  \n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{data['image_name']}:skeleton:mesh', name=AutomaticName('Elastic Strain[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='yy',type=ElasticStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))  \n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))  \n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{data['image_name']}:skeleton:mesh', output=AutomaticName('Elastic Strain[yy]//Average'), destination=OutputStream(filename='{data['output_path']}/bcn2_elastic_strain_yy',mode='w'))  \n" \
        f"OOF.File.Save.Mesh(filename='{data['output_path']}/40_1000K_t2_512_x_dir_mesh_abaqus', mode='w', format='abaqus', mesh='{data['image_name']}:skeleton:mesh')  \n" \
        f"OOF.Subproblem.Set_Solver(subproblem='{data['image_name']}:skeleton:mesh:default', solver_mode=BasicSolverMode(time_stepper=BasicStaticDriver(),matrix_method=BasicIterative(tolerance=1e-13,max_iterations=10000)))  \n" \
        f"OOF.Mesh.Set_Field_Initializer(mesh='{data['image_name']}:skeleton:mesh', field=Displacement, initializer=ConstTwoVectorFieldInit(cx=0.0,cy=0.0))  \n" \
        f"OOF.Mesh.Apply_Field_Initializers(mesh='{data['image_name']}:skeleton:mesh')  \n" \
        f"OOF.Mesh.Solve(mesh='{data['image_name']}:skeleton:mesh', endtime=0.0) \n" \
        f"exit()"

    f = open(f"OOF2/temp_scripts/script", "w")
    f.write(oof2_script_str)
    f.close()
