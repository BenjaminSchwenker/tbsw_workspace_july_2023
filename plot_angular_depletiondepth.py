import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpmath import *
from scipy.optimize import curve_fit

file ='/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/quality_of_alignment_NF.csv'


df_results=pd.read_csv(file)  

def lin_fit(x, a, b):
	return a * x + b

def give_mean(df,col):
    mean=[] 
    for index, row in df.iterrows(): 
        #print(index, row)
        #print(type(row['hres_u_all']))
        val,std = tuple(map(lambda x: pd.to_numeric(x, 'coerce'), row[col][1:-1].split(', ')))
        #print(val,std)
        mean.append(val)
    return mean

def give_error(df,col):
    error=[] 
    for index, row in df.iterrows(): 
        #print(index, row)
        #print(type(row['hres_u_all']))
        val,std = tuple(map(lambda x: pd.to_numeric(x, 'coerce'), row[col][1:-1].split(', ')))
        #print(val,std)
        error.append(std)
    return error
def run_form_df(a):
    if isinstance(a, int) == True:
        return a -278
    else:
        return [el-278 for el in a]

plt.viridis()

##########
plt.figure()

plt.title('mean column cluster size vs $\\theta$')

plt.errorbar([0,10,20,30,40,40,50],give_mean(df_results.iloc[[run_form_df(543),run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(543),run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'), c='#440154',label='W14R12 Cz NF')
plt.errorbar([0,15,30,50],give_mean(df_results.iloc[[run_form_df(493),run_form_df(503),run_form_df(508),run_form_df(507)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(493),run_form_df(503),run_form_df(508),run_form_df(507)]],'hsizeUroi'), c='#30678D',label='W5R9 Epi NF')
plt.errorbar([0,10,20,30,40,50],give_mean(df_results.iloc[[run_form_df(451),run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(451),run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),c='#35B778', label='W5R18 Epi NF')
##plt.plot([10,20,30,40,40,50],give_mean(df_results.iloc[[run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]]),color='red', label='W12R14')

plt.xlabel("$\\theta$ [$^{\circ}$]")
plt.ylabel("mean column cluster size ")

plt.legend()
##plt.show()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u.png')


#plt.show()
##########
plt.figure()
plt.title('mean column cluster size vs tan($\\theta$)')

plt.errorbar([np.tan(0*np.pi/180),np.tan(10*np.pi/180),np.tan(20*np.pi/180),np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(543),run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(543),run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'), marker='.', c='#440154',label='W14R12 Cz NF')
plt.errorbar([np.tan(0*np.pi/180),np.tan(15*np.pi/180),np.tan(30*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(493),run_form_df(503),run_form_df(508),run_form_df(507)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(493),run_form_df(503),run_form_df(508),run_form_df(507)]],'hsizeUroi'), marker='.',c='#30678D',label='W5R9 Epi NF')
plt.errorbar([np.tan(0*np.pi/180),np.tan(10*np.pi/180),np.tan(20*np.pi/180),np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(451),run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(451),run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'), marker='.',c='#35B778', label='W5R18 Epi NF')

plt.axvline(x=np.tan(30*np.pi/180))

plt.xlabel("tan($\\theta$)")
plt.ylabel("mean column cluster size ")

plt.legend()
##plt.show()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan.png')

##########
def d_dep(a,b,c):
    d=(33*(b-c))/np.tan(a)
    print(d)
    return d
tan_list=[np.tan(10*np.pi/180),np.tan(20*np.pi/180),np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)]
tan_list_W5R9=[np.tan(15*np.pi/180),np.tan(30*np.pi/180),np.tan(50*np.pi/180)]
tan_list_W5R18=[np.tan(10*np.pi/180),np.tan(20*np.pi/180),np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)]
col_cluster_mean = give_mean(df_results.iloc[[run_form_df(543),run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi')
col_cluster_mean_W5R9=give_mean(df_results.iloc[[run_form_df(493),run_form_df(503),run_form_df(508),run_form_df(507)]],'hsizeUroi')
col_cluster_mean_W5R18=give_mean(df_results.iloc[[run_form_df(451),run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi')


##########
plt.figure()

plt.title('mean column cluster size u fit')

popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)]),  np.array(give_mean(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi')))
a_2, a_W14R12= popt
error_slope_W14R12=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W12R14_slope=a_2*33
plt.plot(tan_list,[a_W14R12+tan_list[i]*a_2 for i in range(len(tan_list))],c='#440154', label='W14R12 Cz NF fit')


popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(50*np.pi/180)]),  np.array(give_mean(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi')))
a_2,a_W5R9 = popt
error_slope_W5R9=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W5R9_slope=a_2*33
plt.plot(tan_list_W5R9,[a_W5R9+tan_list_W5R9[i]*a_2 for i in range(len(tan_list_W5R9))], c='#30678D',label='W5R9 fit')

popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)]),np.array(give_mean(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi')))
a_2, a_W5R18 = popt
error_slope_W5R18=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W5R18_slope=a_2*33
plt.plot(tan_list_W5R18,[a_W5R18+tan_list_W5R18[i]*a_2 for i in range(len(tan_list_W5R18))],c='#35B778', label='W5R18 fit')


plt.errorbar([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#440154', label='W14R12 Cz NF')
plt.errorbar([np.tan(30*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#30678D', label='W5R9 Epi NF')
plt.errorbar([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#35B778', label='W5R18 Epi NF')


plt.text(0.8, 1.2, 'depleton depth\nW14R12: {}$\pm${}$\pm$ 2\nW5R9: {}$\pm${}$\pm$ 2\nW5R18: {}$\pm${}$\pm$ 2'.format(round(depth_W12R14_slope,2),round(error_slope_W14R12,2),round(depth_W5R9_slope,2),round(error_slope_W5R18,2) ,round(depth_W5R18_slope,2),round(error_slope_W5R18,2)), ha='left', va='top', fontsize=10)

plt.xlabel("tan($\\theta$)")
plt.ylabel("mean column cluster size ")

plt.legend()
##plt.show()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan_fit.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan_fit.png')


##########
plt.figure()

plt.title('mean column cluster size u fit ONLY LOWER 2 POINTS')

popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(40*np.pi/180)]),  np.array(give_mean(df_results.iloc[[run_form_df(555),run_form_df(556)]],'hsizeUroi')))
a_2, a_W14R12= popt
error_slope_W14R12=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W12R14_slope=a_2*33
plt.plot(tan_list,[a_W14R12+tan_list[i]*a_2 for i in range(len(tan_list))],c='#440154', label='W14R12 Cz NF fit')


popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(50*np.pi/180)]),  np.array(give_mean(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi')))
a_2,a_W5R9 = popt
error_slope_W5R9=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W5R9_slope=a_2*33
plt.plot(tan_list_W5R9,[a_W5R9+tan_list_W5R9[i]*a_2 for i in range(len(tan_list_W5R9))], c='#30678D',label='W5R9 fit')

popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(40*np.pi/180)]),np.array(give_mean(df_results.iloc[[run_form_df(460),run_form_df(461)]],'hsizeUroi')))
a_2, a_W5R18 = popt
error_slope_W5R18=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W5R18_slope=a_2*33
plt.plot(tan_list_W5R18,[a_W5R18+tan_list_W5R18[i]*a_2 for i in range(len(tan_list_W5R18))],c='#35B778', label='W5R18 fit')


plt.errorbar([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#440154', label='W14R12 Cz NF')
plt.errorbar([np.tan(30*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#30678D', label='W5R9 Epi NF')
plt.errorbar([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#35B778', label='W5R18 Epi NF')


plt.text(0.8, 1.2, 'depleton depth\nW14R12: {}$\pm${}\nW5R9: {}$\pm${}\nW5R18: {}$\pm${}'.format(round(depth_W12R14_slope,2),round(error_slope_W14R12,2),round(depth_W5R9_slope,2),round(error_slope_W5R18,2) ,round(depth_W5R18_slope,2),round(error_slope_W5R18,2)), ha='left', va='top', fontsize=10)

plt.xlabel("tan($\\theta$)")
plt.ylabel("mean column cluster size ")

plt.legend()
#plt.show()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan_fit_LOWER2POINTS.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan_fit_LOWER2POINTS.png')


##########
plt.figure()

plt.title('mean column cluster size u fit HIGHER 2 POINTS')

popt, pcov = curve_fit(lin_fit, np.array([np.tan(40*np.pi/180),np.tan(50*np.pi/180)]),  np.array(give_mean(df_results.iloc[[run_form_df(557),run_form_df(558)]],'hsizeUroi')))
a_2, a_W14R12= popt
error_slope_W14R12=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W12R14_slope=a_2*33
plt.plot(tan_list,[a_W14R12+tan_list[i]*a_2 for i in range(len(tan_list))],c='#440154', label='W14R12 Cz NF fit')


popt, pcov = curve_fit(lin_fit, np.array([np.tan(30*np.pi/180),np.tan(50*np.pi/180)]),  np.array(give_mean(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi')))
a_2,a_W5R9 = popt
error_slope_W5R9=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W5R9_slope=a_2*33
plt.plot(tan_list_W5R9,[a_W5R9+tan_list_W5R9[i]*a_2 for i in range(len(tan_list_W5R9))], c='#30678D',label='W5R9 fit')

popt, pcov = curve_fit(lin_fit, np.array([np.tan(40*np.pi/180),np.tan(50*np.pi/180)]),np.array(give_mean(df_results.iloc[[run_form_df(461),run_form_df(464)]],'hsizeUroi')))
a_2, a_W5R18 = popt
error_slope_W5R18=np.sqrt(pcov[0,0])
print('slope', a_2, 'depth', a_2*33)
depth_W5R18_slope=a_2*33
plt.plot(tan_list_W5R18,[a_W5R18+tan_list_W5R18[i]*a_2 for i in range(len(tan_list_W5R18))],c='#35B778', label='W5R18 fit')


plt.errorbar([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#440154', label='W14R12 Cz NF')
plt.errorbar([np.tan(30*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(508),run_form_df(507)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#30678D', label='W5R9 Epi NF')
plt.errorbar([np.tan(30*np.pi/180),np.tan(40*np.pi/180),np.tan(50*np.pi/180)],give_mean(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),yerr=give_error(df_results.iloc[[run_form_df(460),run_form_df(461),run_form_df(464)]],'hsizeUroi'),linestyle = 'None',marker="^",c='#35B778', label='W5R18 Epi NF')


plt.text(0.8, 1.2, 'depleton depth\nW14R12: {}$\pm${}\nW5R9: {}$\pm${}\nW5R18: {}$\pm${}'.format(round(depth_W12R14_slope,2),round(error_slope_W14R12,2),round(depth_W5R9_slope,2),round(error_slope_W5R18,2) ,round(depth_W5R18_slope,2),round(error_slope_W5R18,2)), ha='left', va='top', fontsize=10)

plt.xlabel("tan($\\theta$)")
plt.ylabel("mean column cluster size ")

plt.legend()
##plt.show()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan_fit_HIGER2POINTS.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_meancolumnclustersize_u_tan_fit_HIGER2POINTS.png')



##########
plt.figure()

plt.title('depletion depth from fit')




plt.plot(tan_list,[(col_cluster_mean[i]-a_W14R12)*33/tan_list[i] for i in range(len(tan_list))],c='#440154', label='W14R12 Cz NF fit')
plt.plot(tan_list_W5R9,[(col_cluster_mean_W5R9[i]-a_W5R9)*33/tan_list_W5R9[i] for i in range(len(tan_list_W5R9))],c='#30678D', label='W5R9 fit')
plt.plot(tan_list_W5R18,[(col_cluster_mean_W5R18[i]-a_W5R18)*33/tan_list_W5R18[i] for i in range(len(tan_list_W5R18))],c='#35B778', label='W5R18 fit')
plt.axvline(x=np.tan(29*np.pi/180))



plt.xlabel("tan($\\theta$)")
plt.ylabel("depletion depth [µm] ")

plt.legend()
##plt.show()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_depletion_fit.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angularscan_depletion_fit.png')

#############

plt.figure()

#plt.errorbar([10,20,30,40,40,50],give_charge(df_results.iloc[[run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]]),yerr=give_chargeerror(df_results.iloc[[run_form_df(544),run_form_df(554),run_form_df(555),run_form_df(556),run_form_df(557),run_form_df(558)]]), label='W12R14')
plt.errorbar([15,30,50],give_mean(df_results.iloc[[run_form_df(503),run_form_df(508),run_form_df(507)]],'chargeMPV'),yerr=give_error(df_results.iloc[[run_form_df(503),run_form_df(508),run_form_df(507)]],'chargeMPV'), label='W5R9 Epi NF')
plt.errorbar([10,20,30,40],give_mean(df_results.iloc[[run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461)]],'chargeMPV'),yerr=give_error(df_results.iloc[[run_form_df(454),run_form_df(455),run_form_df(460),run_form_df(461)]],'chargeMPV'), label='W5R18 Epi NF')
plt.errorbar([10,20,30,40,50],[24.39,24.82,25.93,29.22,33.06],yerr=[4.05,4.08,4.17,4.03,5.12],color='b', label='Digitizer')

plt.xlabel("$\\theta$ [$^{\circ}$]")
plt.ylabel("cluster charge")

plt.legend()
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angular_cluster.pdf', format="pdf", bbox_inches="tight")  
plt.savefig('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/results/deppletion_depth_NF/angular_cluster.png')
#plt.show()