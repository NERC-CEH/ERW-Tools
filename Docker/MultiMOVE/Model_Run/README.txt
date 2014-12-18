Simple invokation of docker with a wrapper script to pull R packages and install
Files placed on Alpha Spike under /mnt/intput + the MultiMOVE package 

Output placed in /mnt/output

docker run -it -v /mnt/input:/input -v /mnt/output:/output rocker/rstudio Rscript /input/model2.r

docker run -it -v /mnt/input:/input -v /mnt/output:/output scisys/rbase Rscript /input/modelfast.r

