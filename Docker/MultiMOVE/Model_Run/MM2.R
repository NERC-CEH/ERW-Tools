##load the required library
library(MultiMOVE)

##load in datasets from the package - this step might be replaced by the user's own uploaded csv file
data(example_data)
data(BRCtable)

##random pertabation of one input variable for sensitivity analysis.
ran_pert <- rnorm(length(example_data[,1]),0,0.25)
example_data[,1] <- example_data[,1]+ran_pert

##create an empty matrix of probabilities which can be populated in the loop below
out_probs <- matrix(nrow=length(example_data[,1]),ncol=length(BRCtable[,1]))

##loop over all species
for(i in 1:length(BRCtable[,1])){

  ##use multimove to obtain predictions for current species
  output <- try(multiMOVE_predict(example_data,BRC=BRCtable[i,1],map=FALSE))

  ##if multimove ran ok, fill the table with probabilities
  if(class(output)!="try-error"){

      out_probs[,i]=output[,1]

  }

}


## change output table to data frame ready for writing.
out_probs <- data.frame(out_probs)

## give the columns in the output table of probabilities names according to the species number
names(out_probs)=paste("SP",BRCtable[,2],sep="_")

##writew the output table of probabilities to a csv file
write.csv(out_probs,"/output/Output_Probability_Table.csv",row.names=FALSE)


