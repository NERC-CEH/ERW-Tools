#Grab list of packages required
#packages_required = read.table("packages_required")
packages_required <- scan("/tmp/packages_required", what="character")

for (i in 1:length(packages_required)) {
print (packages_required[i])
install.packages(packages_required[i], repos = NULL, type = "source")
}


