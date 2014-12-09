#Test to see if packages are installed, if not do it!
#Define function
is.installed <- function(mypkg) is.element(mypkg, installed.packages()[,1])

#Grab list of packages required
#packages_required = read.table("packages_required")
packages_required <- scan("/tmp/packages_required", what="character")

for (i in 1:length(packages_required)) {
print (packages_required[i])
if (is.installed(packages_required[i])) {
   print ("Package available")
} else {
   print ("Install Package")
   install.packages(packages_required[i])

}
}

