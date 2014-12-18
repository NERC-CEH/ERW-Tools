Scripts and steering file were placed on Alpha Spike model under /mnt/input
Docker invokation of scripts: -
docker run -it -v /mnt/input:/input -v /mnt/output:/output scisys/rbase Rscript /input/R_plot_Density_DataSet_items.r

The Docker container scsisys/rbase was the name given to the MutliMOVE model created by the parent directory

docker build -t scisys/rbase .

Output files created: -
/mnt/output/PlotOut.pdf
/mnt/output/DensityPlotOut.pdf




