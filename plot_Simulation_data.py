import ROOT
import os
import argparse
import re

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser('calibFuncExample.py')
    add_arg = parser.add_argument
    add_arg('-file1', default='Plotter-run000879-roi-105-220-2-510.root', type=str,
            help='data file with path')
    add_arg('-file2', default='Plotter-run000879-roi-105-220-2-510.root', type=str,
            help='simulation file with path')
    return parser.parse_args()

args = parse_args()

# Define the ROOT file path

# Extract the run number from the file name
match = re.search(r'run(\d+)', args.file1)

if match:
    run_number = match.group(1)
    print("Run Number:", run_number)
else:
    print("Run number not found in the filename.")
print(run_number)

# Create a folder to save the PDF
output_folder = "/home/bgnet/tbsw_workspace_july_2023/simulations/comparison/"
os.makedirs(output_folder, exist_ok=True)

# Open the ROOT file
root_file1 = ROOT.TFile(args.file1)
root_file2 = ROOT.TFile(args.file2)

# Access the histograms
hCCharge1 = root_file1.Get("hCCharge")
hCCharge2 = root_file2.Get("hCCharge")

# Normalize the peaks to 1
max_value1 = hCCharge1.GetMaximum()
max_value2 = hCCharge2.GetMaximum()
hCCharge1.Scale(1.0 / max_value1)
hCCharge2.Scale(1.0 / max_value2)

# Create a canvas for drawing the histograms
canvas = ROOT.TCanvas("canvas", "Cluster Charge Plots", 800, 600)

# Set different colors for the histograms
hCCharge1.SetLineColor(ROOT.kBlack)
hCCharge2.SetLineColor(ROOT.kBlue)

# Create a PDF file for the first set of plots
pdf_file_set1 = ROOT.TPDF(os.path.join(output_folder, f"comparison_sim_data_{run_number}.pdf"))

# Loop to create and save the first set of plots in normal and log scale
for log_scale in [False, True]:
    # Set the canvas to log scale on the Y-axis if log_scale is True
    if log_scale:
        canvas.SetLogy()

    # Remove the statistics box for each histogram
    hCCharge1.SetStats(0)
    hCCharge2.SetStats(0)

    # Plot hCCharge with lines connecting the data points
    hCCharge1.Draw("HIST")
    hCCharge1.SetTitle(f"Cluster Charge Comparison (Run {run_number})")
    hCCharge1.GetXaxis().SetTitle("Cluster Charge [electrons]")
    hCCharge1.GetYaxis().SetTitle("Number of Hits")
    hCCharge1.GetYaxis().SetTitleOffset(1.2)

    # Plot hCCharge_size==1 on the same canvas
    hCCharge2.Draw("HIST SAME")

    # Create a legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hCCharge1, "Data", "l")
    legend.AddEntry(hCCharge2, "Simulation", "l")
    legend.Draw()

    # Save the plot to the PDF
    canvas.Update()

# Create a PDF file for the second set of plots in normal scale
canvas.SetLogy(False)

# Plot hCCharge with lines connecting the data points
hCCharge1.Draw("HIST")
hCCharge1.SetTitle(f"Cluster Charge Comparison (Run {run_number})")
hCCharge1.GetXaxis().SetTitle("Cluster Charge [electrons]")
hCCharge1.GetYaxis().SetTitle("Number of Hits")
hCCharge1.GetYaxis().SetTitleOffset(1.2)

# Plot hCCharge_size==1 on the same canvas
hCCharge2.Draw("HIST SAME")

# Create a legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hCCharge1, "Data", "l")
legend.AddEntry(hCCharge2, "Simulation", "l")
legend.Draw()

# Save the plot to the PDF
canvas.Update()

pdf_file_set1.Close()

# Close the ROOT file
root_file1.Close()
root_file2.Close()
