Plot_DataSet_items <- scan("/input/Plot_DataSet_items", what="character")
print(Plot_DataSet_items)

#Read in model data
Output_Probability_Table <- read.csv("/input/Output_Probability_Table.csv")
attach(Output_Probability_Table)
Plot_Colour=heat.colors(length(Plot_DataSet_items))

#Output graph to pdg
pdf(file="/output/DensityPlotOut.pdf")
for (i in 1:length(Plot_DataSet_items)) {
if (i==1) {
   print (Plot_DataSet_items[i])
   print(Plot_Colour[i])
   print(paste0("Output_Probability_Table$",(Plot_DataSet_items[i])))
   colindex = match((Plot_DataSet_items[i]), names(Output_Probability_Table))
   d<-density(Output_Probability_Table[[colindex]])
   plot(d, main="MultiMOVE Probability Density Plot", sub ="Selected sub-specis", ylab="Occurance", xlab="Probability", type="l", col=Plot_Colour[i])
   #plot(paste0("Output_Probability_Table$",(Plot_dataSet_items[i]))
}
else {
   print (Plot_DataSet_items[i])
   colindex = match((Plot_DataSet_items[i]), names(Output_Probability_Table))
   d<-density(Output_Probability_Table[[colindex]])
   lines(d, col=Plot_Colour[i])
}
legend("topright", inset=.05, title="Data Set items", Plot_DataSet_items, fill=Plot_Colour)
}

