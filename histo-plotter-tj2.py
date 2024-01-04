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
parser.add_argument('--calib', default='ToT', type=str, help='Decides range and labels for calibratio in ToT or electron')
parser.add_argument('--iEvt', default=-1, type=int, help='Decides range and labels for calibratio in ToT or electron')
args = parser.parse_args()
  

# Every plotting axis is given as a tuple (nbins,min,max) 
if args.calib == 'ToT':
  DUTConfig = { 'pitch_u' :          0.03304,              # in mm 
              'pitch_v' :          0.03304,              # in mm
              'residual_u_axis':   (151,-0.1,+0.1),    # in mm    
              'residual_v_axis':   (151,-0.1,+0.1),    # in mm 
              'charge_unit':       'ToT / LSB' ,   
              'seed_charge_axis':  (128,0,128),    
              'clus_charge_axis':  (256,0,256), 
              'ucell_axis':        (512,0,512),        
              'vcell_axis':        (512,0,512),       
              'sensor_u_axis':     (512,-0.5*512*0.03304,0.5*512*0.03304),
              'sensor_v_axis':     (512,-0.5*512*0.03304,0.5*512*0.03304), 
            }
elif args.calib == 'electrons':
  DUTConfig = { 'pitch_u' :          0.03304,              # in mm 
              'pitch_v' :          0.03304,              # in mm
              'residual_u_axis':   (151,-0.1,+0.1),    # in mm    
              'residual_v_axis':   (151,-0.1,+0.1),    # in mm 
              'charge_unit':       'electrons' ,   
              'seed_charge_axis':  (50,0,5000),    
              'clus_charge_axis':  (50,0,5000), 
              'ucell_axis':        (512,0,512),        
              'vcell_axis':        (512,0,512),       
              'sensor_u_axis':     (512,-0.5*512*0.03304,0.5*512*0.03304),
              'sensor_v_axis':     (512,-0.5*512*0.03304,0.5*512*0.03304), 
            }
        
if args.calib == 'ToT':
  if args.iEvt > 0:
    #inputfilename="root-files/Histos-TJ2-run{:06d}_clustdb-run{:06d}-run{:06d}_clustdb-reco.root".format(args.runno,args.runno,args.runno)
    inputfilename="root-files/Histos-TJ2-run{:06d}_CoG-run{:06d}-run{:06d}_CoG-reco.root".format(args.runno,args.runno,args.runno)
    
    #histofilename=f"Plotter_iEvt/Plotter-run{args.runno:06d}-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}_{args.iEvt}.root"
    histofilename=f"Plotter_iEvt/Plotter-run{args.runno:06d}_CoG-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}_{args.iEvt}.root"

    #pdffilename=f"Plotter_iEvt/Plotter-run{args.runno:06d}-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}_{args.iEvt}.pdf"
    pdffilename=f"Plotter_iEvt/Plotter-run{args.runno:06d}_CoG-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}_{args.iEvt}.pdf"   
  else:
    #inputfilename="root-files/Histos-TJ2-run{:06d}_clustdb-run{:06d}-run{:06d}_clustdb-reco.root".format(args.runno,args.runno,args.runno)
    inputfilename="root-files/Histos-TJ2-run{:06d}_CoG-run{:06d}-run{:06d}_CoG-reco.root".format(args.runno,args.runno,args.runno)

    #histofilename=f"Plotter/Plotter-run{args.runno:06d}-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.root"
    histofilename=f"Plotter/Plotter-run{args.runno:06d}_CoG-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.root"

    #pdffilename=f"Plotter/Plotter-run{args.runno:06d}-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.pdf"
    pdffilename=f"Plotter/Plotter-run{args.runno:06d}_CoG-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.pdf"   

elif args.calib == 'electrons':
  #inputfilename="root-files/Histos-TJ2-run{:06d}_clustdb_cal-run{:06d}-run{:06d}_clustdb_cal-reco.root".format(args.runno,args.runno,args.runno)
  inputfilename="root-files/Histos-TJ2-run{:06d}_CoG_cal-run{:06d}-run{:06d}_CoG_cal-reco.root".format(args.runno,args.runno,args.runno)

  #histofilename=f"Plotter_cal/Plotter-run{args.runno:06d}-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.root"
  histofilename=f"Plotter_cal/Plotter-run{args.runno:06d}_CoG_cal-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.root"

  #pdffilename=f"Plotter_cal/Plotter-run{args.runno:06d}-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.pdf"
  pdffilename=f"Plotter_cal/Plotter-run{args.runno:06d}_CoG_cal-roi-{args.colstart}-{args.colstop}-{args.rowstart}-{args.rowstop}.pdf"


# Open files with reconstructed run data 
inputfile = ROOT.TFile(inputfilename, 'READ' )   

# Access the TTree containing the event information
tree = inputfile.Get("Hit") 

# Get the maximum value in the iEvt branch
max_iEvt = tree.GetMaximum("iEvt")
# Define the maximum iEvt value for the base cut
max_iEvt_cut = (max_iEvt/100)*args.iEvt

print("The highest number in iEvt is:", max_iEvt)


if args.iEvt > 0:
  # Create one histofile per run  
  histofile = ROOT.TFile( histofilename, 'RECREATE', 'Histos created from file ' + inputfilename )

  # Add residual plots 
  residuals.plot(inputfile, histofile, basecut="hasTrack==0 && iEvt >= {}".format(max_iEvt_cut), Config=DUTConfig)
      
  # Add efficiency plots   
  efficiency.plot(inputfile, histofile, basecut="maskedPixel==0 && iEvt >= {}".format(max_iEvt_cut), matchcut="hasHit==0", uaxis=(512,0,512), vaxis=(512,0,512))
      
  # Add superpixel in-pixel charge plots 
  inpixel.plot_superpixel(inputfile, histofile, pixeltype=0, upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20, ufold=2, vfold=2)             
        
  # Add superpixel in-pixel efficiency plots with event cut
  efficiency.plot_super_inpix(inputfile, histofile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{} && iEvt >= {}".format(args.colstart, args.colstop,args.rowstart,args.rowstop,max_iEvt_cut), matchcut="hasHit==0", upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20)

  # Compute efficiency (and error) in specified ROI
  efficiency.extract_roi(inputfile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{} && iEvt >= {}".format(args.colstart, args.colstop,args.rowstart,args.rowstop,max_iEvt_cut), matchcut="hasHit==0", uaxis=(args.colstop-args.colstart-1,args.colstart,args.colstop), vaxis=(128,args.rowstart,args.rowstop))

  # Make a pdf containing all plots 
  residuals.make_pdf(histofile, pdffilename)

else:  
  # Create one histofile per run  
  histofile = ROOT.TFile( histofilename, 'RECREATE', 'Histos created from file ' + inputfilename )

  # Add residual plots 
  residuals.plot(inputfile, histofile, basecut="hasTrack==0 ", Config=DUTConfig)
  # Add residual plots
  residuals.plot_roi(inputfile, histofile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{}".format(args.colstart, args.colstop,args.rowstart,args.rowstop), Config=DUTConfig)    
  # Add efficiency plots   
  efficiency.plot(inputfile, histofile, basecut="maskedPixel==0", matchcut="hasHit==0", uaxis=(512,0,512), vaxis=(512,0,512))
      
  # Add superpixel in-pixel charge plots 
  inpixel.plot_superpixel(inputfile, histofile, pixeltype=0, upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20, ufold=2, vfold=2)             
        
  # Add superpixel in-pixel efficiency plots
  efficiency.plot_super_inpix(inputfile, histofile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{}".format(args.colstart, args.colstop,args.rowstart,args.rowstop), matchcut="hasHit==0", upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20)

  # Add superpixel in-pixel efficiency plots with event cut
  #efficiency.plot_super_inpix(inputfile, histofile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{} && iEvt >= {}".format(args.colstart, args.colstop,args.rowstart,args.rowstop,max_iEvt_cut), matchcut="hasHit==0", upitch=DUTConfig['pitch_u'], vpitch=DUTConfig['pitch_v'], ubins=20, vbins=20)

  # Compute efficiency (and error) in specified ROI
  efficiency.extract_roi(inputfile, basecut="maskedPixel==0 && cellU_fit>{} && cellU_fit<{} && cellV_fit> {} && cellV_fit<{}".format(args.colstart, args.colstop,args.rowstart,args.rowstop), matchcut="hasHit==0", uaxis=(args.colstop-args.colstart-1,args.colstart,args.colstop), vaxis=(128,args.rowstart,args.rowstop))


  # Make a pdf containing all plots 
  residuals.make_pdf(histofile, pdffilename)

# Close all files 
histofile.Write()
histofile.Close()
inputfile.Close()
