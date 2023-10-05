
def load(img_name, output_path):
    oof2_script_str = f"OOF.Windows.Graphics.New()\n" \
        f"OOF.Graphics_1.Toolbox.Pixel_Select.Burn(source='{img_name}:{img_name}', local_flammability=0.1, global_flammability=0.2, color_space_norm='L1', next_nearest=False, points=[Point(1,1)], shift=0, ctrl=0)\n" \
        f"OOF.PixelGroup.New(name='gamma', microstructure='{img_name}')\n" \
        f"OOF.PixelGroup.AddSelection(microstructure='{img_name}', group='gamma')\n" \
        f"OOF.Graphics_1.Toolbox.Pixel_Select.Invert(source='{img_name}')\n" \
        f"OOF.PixelGroup.New(name='gamma_prime', microstructure='{img_name}')\n" \
        f"OOF.PixelGroup.AddSelection(microstructure='{img_name}', group='gamma_prime')\n" \
        f"OOF.Material.New(name='gamma_1000k', material_type='bulk')\n" \
        f"OOF.Material.New(name='gamma_prime_1000k', material_type='bulk')\n" \
        f"OOF.Property.Copy(property='Mechanical:Elasticity:Anisotropic:Cubic', new_name='gamma')\n" \
        f"OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.gamma(cijkl=CubicRank4TensorCij(c11=208800000000.0,c12=148830000000.0,c44=96240000000.0))\n" \
        f"OOF.Property.Copy(property='Orientation', new_name='gamma')\n" \
        f"OOF.Property.Parametrize.Orientation.gamma(angles=XYZ(phi=0,theta=0,psi=0))\n" \
        f"OOF.Material.Add_property(name='gamma_1000k', property='Orientation:gamma')\n" \
        f"OOF.Material.Add_property(name='gamma_1000k', property='Mechanical:Elasticity:Anisotropic:Cubic:gamma')\n" \
        f"OOF.Property.Copy(property='Mechanical:Elasticity:Anisotropic:Cubic', new_name='gamma_prime')\n" \
        f"OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Cubic.gamma_prime(cijkl=CubicRank4TensorCij(c11=207630000000.0,c12=149400000000.0,c44=101970000000.0))\n" \
        f"OOF.Property.Copy(property='Orientation', new_name='gamma_prime')\n" \
        f"OOF.Property.Parametrize.Orientation.gamma_prime(angles=XYZ(phi=0,theta=0,psi=0))\n" \
        f"OOF.Material.Add_property(name='gamma_prime_1000k', property='Orientation:gamma_prime')\n" \
        f"OOF.Material.Add_property(name='gamma_prime_1000k', property='Mechanical:Elasticity:Anisotropic:Cubic:gamma_prime')\n" \
        f"OOF.Material.Assign(material='gamma_prime_1000k', microstructure='{img_name}', pixels='gamma_prime')\n" \
        f"OOF.Material.Assign(material='gamma_1000k', microstructure='{img_name}', pixels='gamma')\n" \
        f"OOF.Skeleton.New(name='skeleton', microstructure='{img_name}', x_elements=50, y_elements=50, skeleton_geometry=QuadSkeleton(left_right_periodicity=True,top_bottom_periodicity=True))\n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{img_name}:skeleton', threshold=0.9)\n" \
        f"OOF.Skeleton.Modify(skeleton='{img_name}:skeleton', modifier=Refine(targets=CheckSelectedElements(),criterion=Unconditionally(),degree=Trisection(rule_set='conservative'),alpha=0.5))\n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{img_name}:skeleton', threshold=0.9)\n" \
        f"OOF.Skeleton.Modify(skeleton='{img_name}:skeleton', modifier=Refine(targets=CheckSelectedElements(),criterion=Unconditionally(),degree=Trisection(rule_set='conservative'),alpha=0.5))\n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{img_name}:skeleton', threshold=0.9)\n" \
        f"OOF.Skeleton.Modify(skeleton='{img_name}:skeleton', modifier=SnapNodes(targets=SnapSelected(),criterion=AverageEnergy(alpha=0.5)))\n" \
        f"OOF.ElementSelection.Select_by_Homogeneity(skeleton='{img_name}:skeleton', threshold=0.9)\n" \
        f"OOF.Skeleton.Modify(skeleton='{img_name}:skeleton', modifier=Anneal(targets=FiddleSelectedElements(),criterion=AverageEnergy(alpha=0.5),T=0.0,delta=1.0,iteration=FixedIteration(iterations=5)))\n" \
        f"OOF.Skeleton.Modify(skeleton='{img_name}:skeleton', modifier=Rationalize(targets=AllElements(),criterion=AverageEnergy(alpha=0.5),method=SpecificRationalization(rationalizers=[RemoveShortSide(ratio=5.0), QuadSplit(angle=150), RemoveBadTriangle(acute_angle=15,obtuse_angle=150)])))\n" \
        f"OOF.Skeleton.Modify(skeleton='{img_name}:skeleton', modifier=FixIllegal())\n" \
        f"OOF.Mesh.New(name='mesh', skeleton='{img_name}:skeleton', element_types=['D2_2', 'T3_3', 'Q4_4'])\n" \
        f"OOF.Subproblem.Field.Define(subproblem='{img_name}:skeleton:mesh:default', field=Displacement)\n" \
        f"OOF.Subproblem.Field.Activate(subproblem='{img_name}:skeleton:mesh:default', field=Displacement)\n" \
        f"OOF.Subproblem.Equation.Activate(subproblem='{img_name}:skeleton:mesh:default', equation=Force_Balance)\n" \
        f"OOF.Subproblem.Equation.Activate(subproblem='{img_name}:skeleton:mesh:default', equation=Plane_Stress\n)\n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc', mesh='{img_name}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='x',equation=Force_Balance,eqn_component='x',profile=ConstantProfile(value=-10.0),boundary='left'))\n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc<2>', mesh='{img_name}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='x',equation=Force_Balance,eqn_component='x',profile=ConstantProfile(value=10.0),boundary='right'))\n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc<3>', mesh='{img_name}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='y',equation=Force_Balance,eqn_component='y',profile=ConstantProfile(value=-4.17),boundary='top'))\n" \
        f"OOF.Mesh.Boundary_Conditions.New(name='bc<4>', mesh='{img_name}:skeleton:mesh', condition=DirichletBC(field=Displacement,field_component='y',equation=Force_Balance,eqn_component='y',profile=ConstantProfile(value=4.17),boundary='bottom'))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('GraphicsUpdate'), output=GraphicsUpdate())\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('GraphicsUpdate'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('Stress[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Flux:Component',component='xx',flux=Stress),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Stress[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Stress[xx]//Average'), destination=OutputStream(filename='{output_path}/stress_xx ',mode='w'))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('Stress[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Flux:Component',component='yy',flux=Stress),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Stress[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Stress[yy]//Average'), destination=OutputStream(filename='{output_path}/stress_yy ',mode='w'))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('Geometric Strain[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='xx',type=GeometricStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Geometric Strain[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Geometric Strain[xx]//Average'), destination=OutputStream(filename='{output_path}/strain_xx',mode='w'))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('Geometric Strain[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='yy',type=GeometricStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Geometric Strain[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Geometric Strain[yy]//Average'), destination=OutputStream(filename='{output_path}/strain_yy',mode='w'))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('Elastic Strain[xx]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='xx',type=ElasticStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Elastic Strain[xx]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Elastic Strain[xx]//Average'), destination=OutputStream(filename='{output_path}/elastic_strain_xx',mode='w'))\n" \
        f"OOF.Mesh.Scheduled_Output.New(mesh='{img_name}:skeleton:mesh', name=AutomaticName('Elastic Strain[yy]//Average'), output=BulkAnalysis(output_type='Scalar',data=getOutput('Strain:Component',component='yy',type=ElasticStrain()),operation=AverageOutput(),domain=EntireMesh(),sampling=ElementSampleSet(order=automatic)))\n" \
        f"OOF.Mesh.Scheduled_Output.Schedule.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Elastic Strain[yy]//Average'), scheduletype=AbsoluteOutputSchedule(), schedule=Once(time=0.0))\n" \
        f"OOF.Mesh.Scheduled_Output.Destination.Set(mesh='{img_name}:skeleton:mesh', output=AutomaticName('Elastic Strain[yy]//Average'), destination=OutputStream(filename='{output_path}/elastic_strain_yy',mode='w'))\n" \
        f"OOF.File.Save.Mesh(filename='{output_path}/mesh_abaqus', mode='w', format='abaqus', mesh='{img_name}:skeleton:mesh')\n" \
        f"OOF.Subproblem.Set_Solver(subproblem='{img_name}:skeleton:mesh:default', solver_mode=BasicSolverMode(time_stepper=BasicStaticDriver(),matrix_method=BasicIterative(tolerance=1e-13,max_iterations=10000)))\n" \
        f"OOF.Mesh.Set_Field_Initializer(mesh='{img_name}:skeleton:mesh', field=Displacement, initializer=ConstTwoVectorFieldInit(cx=0.0,cy=0.0))\n" \
        f"OOF.Mesh.Apply_Field_Initializers(mesh='{img_name}:skeleton:mesh')\n" \
        f"OOF.Mesh.Solve(mesh='{img_name}:skeleton:mesh', endtime=0.0)\n"

    f = open("OOF2/temp_scripts/script", "w")
    f.write(oof2_script_str)
    f.close()
