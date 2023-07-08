"""
Simple script for plotting testbeam data using fully reconstructed root files 
from folder root-files. 

All DUT specific adjustements can be made in the DUTConfig dictionary. The 
plotter assumes pixel matrix with rectangular pixels.  

python histo-plotter-tj2.py --colstart 320  --colstop 420 --runno=826

Author: Benjamin Schwenker <benjamin.schwenker@phys.uni-goettingen.de>  
"""


import tbsw.residuals as residuals
import tbsw.efficiency as efficiency
import tbsw.inpixel as inpixel
import ROOT
import os
import glob

import argparse
parser = argparse.ArgumentParser(description="Perform plotting of test beam runs")

parser.add_argument('--runno', dest='runno', type=int, help='Run number')
parser.add_argument('--colstart', default=110, type=int, help='Start/Lower column of ROI for efficiency')
parser.add_argument('--colstop', default=200, type=int, help='Stop/Upper column of ROI for efficiency')
parser.add_argument('--rowstart', default=1, type=int, help='Start/Lower row of ROI for efficiency')
parser.add_argument('--rowstop', default=400, type=int, help='Stop/Upper row of ROI for efficiency')
args = parser.parse_args()
  

# Every plotting axis is given as a tuple (nbins,min,max) 
DUTConfig = { 'pitch_u' :          0.033,              # in mm 
              'pitch_v' :          0.033,              # in mm
              'residual_u_axis':   (151,-0.1,+0.1),    # in mm    
              'residual_v_axis':   (151,-0.1,+0.1),    # in mm 
              'charge_unit':       'ToT / LSB',   
              'seed_charge_axis':  (128,0,128),    
              'clus_charge_axis':  (256,0,256), 
              'ucell_axis':        (512,0,512),        
              'vcell_axis':        (512,0,512),       
              'sensor_u_axis':     (512,-0.5*512*0.033,0.5*512*0.033),
              'sensor_v_axis':     (512,-0.5*512*0.033,0.5*512*0.033), 
            }
        
inputfilename="root-files/Histos-TJ2-run{:06d}-run{:06d}-run{:06d}-reco.root".format(args.runno,args.runno,args.runno)
    
# Open files with reconstructed run data 
inputfile = ROOT.TFile( inputfilename, 'READ' )    
    
# Create one histofile per run  
histofile = ROOT.TFile( 'Plotter-' + os.path.basename(inputfilename), 'RECREATE', 'Histos created from file ' + inputfilename )
    
# Add residual plots 
residuals.plot(inputfile, histofile, basecut="hasTrack==0 && localChi2<20", Config=DUTConfig)
    
# Add efficiency plots   
efficiency.plot(inputfile, histofile, basecut="", matchcut="hasHit==0 && maskedPixel==0", uaxis=(512,0,512), vaxis=(512,0,512))
    
# Add superpixel in-pixel charge plots 
inpixel.plot_superpixel(inputfile, histofile, pixeltype=0, upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20, ufold=2, vfold=2)             
      
# Add superpixel in-pixel efficiency plots 
efficiency.plot_super_inpix(inputfile, histofile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{}".format(args.colstart, args.colstop,args.rowstart,args.rowstop), matchcut="hasHit==0 && localChi2<20", upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20)

# Compute efficiency (and error) in specified ROI
efficiency.extract_roi(inputfile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{}".format(args.colstart, args.colstop,args.rowstart,args.rowstop), matchcut="hasHit==0 && localChi2<20")

# Make a pdf containing all plots 
pdfName = os.path.splitext( os.path.basename( inputfilename ) )[0] + '.pdf' 
residuals.make_pdf(histofile, pdfName)

# Close all files 
histofile.Write()
histofile.Close()
inputfile.Close()
