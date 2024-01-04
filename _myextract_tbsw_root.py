import ROOT
import pandas as pd
from argparse import ArgumentParser
import numpy as np

# usage python3 extract_root.py --start 297 --end 297 --path /home/yannik/vtx/testbeam/data/monopix2/test
#/home/bgnet/workspace-test/root-files

selected_keys = {
"hres_u_all":'RMS',
"hfit_sigma_u":'Mean',
"hres_v_all":'RMS',
"hfit_sigma_v":'Mean',
"hCharge":'Mean',
"hCCharge":'Mean',
"hsize":'Mean',
"hsizeU":'Mean',
"hsizeV":'Mean',
"h2_efficiencymap":'TH2',
"g_efficiency_roi": 'eROI',
}

def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(description='Crawl root files')
    add_arg = parser.add_argument
    add_arg('-s', '--start', type=int, default=1, help='Start run')
    add_arg('-e', '--end', type=int, default=2, help='End run')
    add_arg('-p', '--path', type=str, default='', help='Path to root files')
    return parser.parse_args()


def get_object(path,runs):
    if not path.endswith('/'):
        path=path+'/'
    columns = [x.split('/')[-1] for x in selected_keys.keys()]
    df = pd.DataFrame(columns=columns, index=runs)

    #root_files = ['Plotter-Histos-TJ2-run000{0}_clustdb-run000{0}-run000{0}_clustdb-reco.root'.format(x) for x in runs]
    root_files = ['Plotter-Histos-TJ2-run000{0}-run000{0}-run000{0}-reco.root'.format(x) for x in runs]

    for i,file in enumerate(root_files):
        try:
            f = ROOT.TFile(path+file)
        except Exception:
            continue
        list_per_file = []
        for key in selected_keys.keys():
            plot = f.Get(key)
            #print(key)
            if selected_keys[key] == 'RMS' or selected_keys[key] == 'Mean':
                attr = getattr(plot,"Get%s" % selected_keys[key])
                error = getattr(plot,"Get%sError" % selected_keys[key])
                val = attr()
                list_per_file.append(val)
                #print(val)
            elif selected_keys[key] == 'Efficiency':
                x_start = 100
                x_stop = 200
                y_start = 300
                y_stop = 400
                val_pixels = []
                for x in range(x_start,x_stop,1):
                    if x==225:
                        continue
                    for y in range(y_start,y_stop,1):
                        global_bin = plot.GetGlobalBin(x,y)
                        val_single_pixel = plot.GetEfficiency(global_bin)
                        error_low = plot.GetEfficiencyErrorLow(global_bin)
                        error_high = plot.GetEfficiencyErrorHigh(global_bin)
                        if val_single_pixel>0.0001:
                            #if val_single_pixel>0.00001:
                            val_pixels.append(val_single_pixel)
                if(len(val_pixels)!=0):
                    list_per_file.append(sum(val_pixels)/len(val_pixels))
                else:
                    list_per_file.append(0)

            elif selected_keys[key] == 'eROI':
                roi_effi = plot.GetPointY(0)
                list_per_file.append(roi_effi)
            elif selected_keys[key] == 'TH2':
                x_start = 20
                x_stop = 70
                y_start = 80
                y_stop = 120
                val_pixels = []
                for x in range(x_start,x_stop,1):
                    if x==225:
                        continue
                    for y in range(y_start,y_stop,1):
                        #global_bin = plot.GetGlobalBin(x,y)
                        val_single_pixel = plot.GetBinContent(x,y)
                        #error_low = plot.GetEfficiencyErrorLow(global_bin)
                        #error_high = plot.GetEfficiencyErrorHigh(global_bin)
                        if val_single_pixel>0.0001:
                            #if val_single_pixel>0.00001:
                            val_pixels.append(val_single_pixel)
                if(len(val_pixels)!=0):
                    list_per_file.append(sum(val_pixels)/len(val_pixels))
                else:
                    list_per_file.append(0)

            elif selected_keys[key] == 'single_Efficiency':
                global_bin = plot.GetGlobalBin(1,1)
                val_single_pixel = plot.GetEfficiency(global_bin)
                error_low = plot.GetEfficiencyErrorLow(global_bin)
                error_high = plot.GetEfficiencyErrorHigh(global_bin)
                list_per_file.append(val_single_pixel)
        df.loc[runs[i]] = list_per_file
    return df


if __name__ == '__main__':

    args = parse_args()
    result_df = get_object(args.path,list(range(args.start,args.end+1)))
    
    result_df_res = pd.DataFrame()
    result_df_cluster = pd.DataFrame()
    result_df_eff = pd.DataFrame()

    result_df_res['residualsX'] = result_df['residualsX']
    result_df_res['residualsX1pix'] = result_df['residualsX1pix']
    result_df_res['residualsX2pix'] = result_df['residualsX2pix']
    result_df_res['residualsX3pix'] = result_df['residualsX3pix']
    result_df_res['residualsY'] = result_df['residualsY']
    result_df_res['residualsY1pix'] = result_df['residualsY1pix']
    result_df_res['residualsY2pix'] = result_df['residualsY2pix']
    result_df_res['residualsY3pix'] = result_df['residualsY3pix']

    result_df_cluster['clusterChargeAssociated'] = result_df['clusterChargeAssociated']
    result_df_cluster['seedChargeAssociated'] = result_df['seedChargeAssociated']
    result_df_cluster['clusterSizeAssociated'] = result_df['clusterSizeAssociated']
    result_df_cluster['clusterWidthRowAssociated'] = result_df['clusterWidthRowAssociated']
    result_df_cluster['clusterWidthColAssociated'] = result_df['clusterWidthColAssociated']

    result_df_eff['pixelEfficiencyMap_trackPos'] = result_df['pixelEfficiencyMap_trackPos']
    result_df_eff['chipEfficiencyMap_trackPos'] = result_df['chipEfficiencyMap_trackPos']
    result_df_eff['distanceTrackHit2D'] = result_df['distanceTrackHit2D']
    result_df_eff['eTotalEfficiency'] = result_df['eTotalEfficiency']
    result_df_eff['efficiencyColumns'] = result_df['efficiencyColumns']
    result_df_eff['efficiencyRows'] = result_df['efficiencyRows']

    print(result_df_res.to_markdown())
    print('\n')
    print(result_df_cluster.to_markdown())
    print('\n')
    print(result_df_eff.to_markdown())
    #print(tabulate(result_df, headers='keys', tablefmt='psql'))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
