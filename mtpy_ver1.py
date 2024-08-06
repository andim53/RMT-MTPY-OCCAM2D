import mtpy.modeling.occam2d as occam2d

#edipath = "./edited_transfer_functions_new_throw_error_stat_name/profile2"
#edipath = "./DataEdiBaru/Profile1"
#edipath = "./transfer_function"
#edipath = "./transfer_function2"
edipath = "./DataEdiBaru4"



#ranges = [(1,2,3,4,5,6), (7,8,9,10,11,12), (13,14,15,16,17,18)]
#ranges = [(7,8,10,11,12)]

#ranges = [(1,2,3,4,5,6)] # Profile 1
ranges = [(7,8,9,10,11,12)] # Profile 2
#ranges = [(13,14,15,16,17,18)] # Profile 3

slist = []
for profile_id, ranges in enumerate(ranges, start=1):
    for i in ranges:
        filename = f"stat{i:02}.edi"
        slist.append(filename)

############### Data from edi
ocd = occam2d.Data(edi_path=edipath, station_list=slist)

#ocd.model_mode = '3' # Re_tip, Pseudo Matlab works on this mode 
ocd.model_mode = '4' # for matlab pseudo
#ocd.model_mode = '7' # Re_tip
ocd.save_path = r"./"
ocd.write_data_file()

############### Data from Data

#ocd = occam2d.Data()
#data_fn = "./OccamRun/profile2/PROFILE2.dat"
#ocd = occam2d.Data(data_fn=data_fn, station_list=slist)

#ocd = ocd.read_data_file(data_fn=data_fn)

############### Mesh
ocm = occam2d.Mesh(ocd.station_locations)

# add in elevation
ocm.elevation_profile = ocd.elevation_profile

# change number of layers        
#ocm.n_layers = 110
#ocm.n_layers = 85
ocm.n_layers = 220

# change cell width in station area
#ocm.cell_width = 200
#ocm.cell_width = 100
ocm.cell_width = 500

ocm.build_mesh()
ocm.plot_mesh()
ocm.save_path = ocd.save_path
ocm.write_mesh_file()

############### Profile
# profile = occam2d.Profile(edi_path=edipath, station_list=slist)
# profile.generate_profile()

############### Regularization/Model
# profile = occam2d.Profile(edi_path=edipath, station_list=slist)
# profile.generate_profile()
ocd.generate_profile()
#reg = occam2d.Regularization(profile.station_locations)
reg = occam2d.Regularization(ocd.station_locations)
reg.build_mesh()
reg.build_regularization()
reg.save_path = r"./"
reg.mesh_fn = ocm.mesh_fn
reg.write_regularization_file()

############### Startup
startup = occam2d.Startup()
startup.data_fn = ocd.data_fn
#startup.model_fn = profile.reg_fn
startup.model_fn = reg.reg_fn
#startup.param_count = profile.num_free_param
startup.param_count = reg.num_free_param
startup.save_path = r"./"
startup.write_startup_file()

print("success")