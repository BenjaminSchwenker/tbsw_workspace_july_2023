
start = $1
stop = $2


for i in {start..stop}
do
   python3 tj2-reco.py   --runno $i  --gearfile gear_geoid36.xml
   python histo-plotter-tj2.py --colstart 460  --colstop 475 --runno=$i
done

