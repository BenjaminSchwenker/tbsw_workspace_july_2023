import ROOT
import os
import argparse
import re

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser('calibFuncExample.py')
    add_arg = parser.add_argument
    for i in range(994, 1009):
        if i<=999:
            add_arg(f'-file{i}', default=f'/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/Plotter-run000{i}-roi-482-494-2-510.root', type=str,
                help=f'data or simulation file {i} with path')
        else:
            add_arg(f'-file{i}', default=f'/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/Plotter-run00{i}-roi-482-494-2-510.root', type=str,
                help=f'data or simulation file {i} with path')
    return parser.parse_args()

args = parse_args()

# Create a folder to save the PDF
output_folder = "/home/bgnet/tbsw_workspace_july_2023/BIAS_Scan"
os.makedirs(output_folder, exist_ok=True)

# Open the ROOT files
root_files = [ROOT.TFile(getattr(args, f'file{i}')) for i in range(994, 1009)]

# Access the histograms
hCCharges = [root_file.Get("hCChargeroi") for root_file in root_files]

# Normalize the peaks to 1
max_values = [h.GetMaximum() for h in hCCharges]
for i, h in enumerate(hCCharges):
    h.Scale(1.0 / max_values[i])
# Normalize the peaks to 1
max_values = [h.GetMaximum() for h in hCCharges]

# Set different colors for the histograms
colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kCyan, ROOT.kMagenta, ROOT.kYellow, ROOT.kPink, ROOT.kAzure]

# Repeat colors if there are more files than colors
while len(colors) < len(hCCharges):
    colors += colors

for i, h in enumerate(hCCharges):
    h.SetLineColor(colors[i])

# Create a canvas for drawing the histograms
canvas = ROOT.TCanvas("canvas", "Cluster Charge Plots", 800, 600)


for i, h in enumerate(hCCharges):
    h.SetLineColor(colors[i])

# Create a PDF file for the plots
pdf_file = ROOT.TPDF(os.path.join(output_folder, f"W08_R19_BIAS_HV_994-1008.pdf"))

# Loop to create and save the plots in normal and log scale
for log_scale in [False, True]:
    # Set the canvas to log scale on the Y-axis if log_scale is True
    if log_scale:
        canvas.SetLogy()

    # Remove the statistics box for each histogram
    for h in hCCharges:
        h.SetStats(0)

    # Plot histograms with lines connecting the data points
    hCCharges[0].Draw("HIST")
    hCCharges[0].SetTitle(f"BIAS_HV 994-1008")
    hCCharges[0].GetXaxis().SetTitle("Cluster Charge [electrons]")
    hCCharges[0].GetYaxis().SetTitle("Number of Hits")
    hCCharges[0].GetYaxis().SetTitleOffset(1.2)

    for i in range(1, 15):
        hCCharges[i].Draw(f"HIST SAME")

    # Create a legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hCCharges[0], f"BIAS_HV 2", "l")
    for i in range(1, 15):
        legend.AddEntry(hCCharges[i], f"BIAS_HV {i*2+2}", "l")
    legend.Draw()

    # Save the plot to the PDF
    canvas.Update()

# Individual plots for each file with correct labels
for i, h in enumerate(hCCharges):
    canvas.SetLogy(False)
    h.SetStats(0)
    h.Draw("HIST")
    h.SetTitle(f"BIAS_HV {i*2+2}")
    h.GetXaxis().SetTitle("Cluster Charge [electrons]")
    h.GetYaxis().SetTitle("Number of Hits")
    h.GetYaxis().SetTitleOffset(1.2)
    canvas.Update()

# Plot every second file
canvas.SetLogy(False)
hCCharges[0].SetStats(0)
hCCharges[0].Draw("HIST")
hCCharges[0].SetTitle(f"BIAS_HV 994")
hCCharges[0].GetXaxis().SetTitle("Cluster Charge [electrons]")
hCCharges[0].GetYaxis().SetTitle("Number of Hits")
hCCharges[0].GetYaxis().SetTitleOffset(1.2)

for i in range(2, 15, 2):
    hCCharges[i].Draw(f"HIST SAME")

legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hCCharges[0], f"BIAS_HV 2", "l")
for i in range(2, 15, 2):
    legend.AddEntry(hCCharges[i], f"BIAS_HV {i*2+2}", "l")
legend.Draw()

canvas.Update()

# Plot every second file
canvas.SetLogy(False)
hCCharges[1].SetStats(0)
hCCharges[1].Draw("HIST")
hCCharges[1].SetTitle(f"BIAS_HV 996")
hCCharges[1].GetXaxis().SetTitle("Cluster Charge [electrons]")
hCCharges[1].GetYaxis().SetTitle("Number of Hits")
hCCharges[1].GetYaxis().SetTitleOffset(1.2)

for i in range(3, 14, 2):
    hCCharges[i].Draw(f"HIST SAME")

legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hCCharges[1], f"BIAS_HV 4", "l")
for i in range(3, 14, 2):
    legend.AddEntry(hCCharges[i], f"BIAS_HV {i*2+2}", "l")
legend.Draw()

canvas.Update()

# Close the PDF file
pdf_file.Close()

# Close the ROOT files
for root_file in root_files:
    root_file.Close()
