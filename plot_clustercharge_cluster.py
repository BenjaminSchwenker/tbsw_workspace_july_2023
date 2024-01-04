import ROOT
import os
import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser('calibFuncExample.py')
    add_arg = parser.add_argument
    add_arg('-path', default="/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/", type=str, help='folder path')
    add_arg('-file', default='Plotter-run000879-roi-105-220-2-510.root', type=str,
            help='file in folder')
    return parser.parse_args()

args = parse_args()
# Define the ROOT file path
root_file_path = os.path.join(args.path, args.file)

# Extract the run number from the file name
run_number = os.path.splitext(os.path.basename(root_file_path))[0].split('-')[1]
print(run_number)

# Create a folder to save the PDF
output_folder = "Plotter_clustercalibration"
os.makedirs(output_folder, exist_ok=True)

# Open the ROOT file
root_file = ROOT.TFile(root_file_path)

# Access the histograms
hCCharge = root_file.Get("hCCharge")
hCCharge_size1 = root_file.Get("hCCharge_size==1")
hCCharge_size_gt1 = root_file.Get("hCCharge_size>1")
hCCharge_size2 = root_file.Get("hCCharge_size==2")
hCCharge_size_gt2 = root_file.Get("hCCharge_size>=2")
hCCharge_size3 = root_file.Get("hCCharge_size==3")
hCCharge_size_gt3 = root_file.Get("hCCharge_size>=3")
hCCharge_size4 = root_file.Get("hCCharge_size==4")
hCCharge_size_gt4 = root_file.Get("hCCharge_size>=4")

# Create a canvas for drawing the histograms
canvas = ROOT.TCanvas("canvas", "Cluster Charge Plots", 800, 600)

# Set different colors for the histograms
hCCharge.SetLineColor(ROOT.kBlack)
hCCharge_size1.SetLineColor(ROOT.kBlue)
hCCharge_size_gt1.SetLineColor(ROOT.kGreen)
hCCharge_size2.SetLineColor(ROOT.kGreen)
hCCharge_size_gt2.SetLineColor(ROOT.kGreen)
hCCharge_size3.SetLineColor(ROOT.kRed)
hCCharge_size4.SetLineColor(ROOT.kMagenta)


# Create a PDF file for the first set of plots
pdf_file_set1 = ROOT.TPDF(os.path.join(output_folder, f"cluster_charge_run{run_number}.pdf"))

# Loop to create and save the first set of plots in normal and log scale
for log_scale in [False, True]:
    # Set the canvas to log scale on the Y-axis if log_scale is True
    if log_scale:
        canvas.SetLogy()

    # Remove the statistics box for each histogram
    hCCharge.SetStats(0)
    hCCharge_size1.SetStats(0)
    hCCharge_size_gt1.SetStats(0)

    # Plot hCCharge
    hCCharge.Draw()
    hCCharge.SetTitle(f"Cluster Charge Comparison (Run {run_number})")
    hCCharge.GetXaxis().SetTitle("Cluster Charge [electrons]")
    hCCharge.GetYaxis().SetTitle("Number of Hits")
    hCCharge.GetYaxis().SetTitleOffset(1.2)

    # Plot hCCharge_size==1 on the same canvas
    hCCharge_size1.Draw("SAME")

    # Plot hCCharge_size>1 on the same canvas
    hCCharge_size_gt1.Draw("SAME")

    # Create a legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hCCharge, "All Clusters", "l")
    legend.AddEntry(hCCharge_size1, "Size == 1", "l")
    legend.AddEntry(hCCharge_size_gt1, "Size > 1", "l")
    legend.Draw()

    # Save the plot to the PDF
    canvas.Update()


# Create a PDF file for the second set of plots in normal scale
canvas.SetLogy(False)

# Plot hCCharge
hCCharge.Draw()
hCCharge.SetTitle(f"Cluster Charge Comparison (Run {run_number})")
hCCharge.GetXaxis().SetTitle("Cluster Charge [electrons]")
hCCharge.GetYaxis().SetTitle("Number of Hits")
hCCharge.GetYaxis().SetTitleOffset(1.2)

# Plot hCCharge_size==1 on the same canvas
hCCharge_size1.Draw("SAME")
hCCharge_size2.Draw("SAME")
hCCharge_size3.Draw("SAME")
hCCharge_size4.Draw("SAME")

# Create a legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hCCharge, "All Clusters", "l")
legend.AddEntry(hCCharge_size1, "Size == 1", "l")
legend.AddEntry(hCCharge_size2, "Size == 2", "l")
legend.AddEntry(hCCharge_size3, "Size == 3", "l")
legend.AddEntry(hCCharge_size4, "Size == 4", "l")
legend.Draw()

# Save the plot to the PDF
canvas.Update()


# Plot the second set with only the second plot on log scale
canvas.SetLogy(True)

# Remove the statistics box for each histogram
hCCharge.SetStats(0)
hCCharge_size1.SetStats(0)
hCCharge_size2.SetStats(0)

# Plot hCCharge
hCCharge.Draw()
hCCharge.SetTitle(f"Cluster Charge Comparison (Run {run_number})")
hCCharge.GetXaxis().SetTitle("Cluster Charge [electrons]")
hCCharge.GetYaxis().SetTitle("Number of Hits")
hCCharge.GetYaxis().SetTitleOffset(1.2)

# Plot hCCharge_size==1 on the same canvas
hCCharge_size1.Draw("SAME")
hCCharge_size2.Draw("SAME")
hCCharge_size3.Draw("SAME")
hCCharge_size4.Draw("SAME")

# Create a legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(hCCharge, "All Clusters", "l")
legend.AddEntry(hCCharge_size1, "Size == 1", "l")
legend.AddEntry(hCCharge_size2, "Size == 2", "l")
legend.AddEntry(hCCharge_size3, "Size == 3", "l")
legend.AddEntry(hCCharge_size4, "Size == 4", "l")
legend.Draw()

# Save the plot to the PDF
canvas.Update()



pdf_file_set1.Close()

# Close the ROOT file
root_file.Close()
