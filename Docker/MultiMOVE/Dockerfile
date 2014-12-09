## Start with the rocker image providing 'base R' using a small Debian testing installation and the current R release
FROM r-base:latest

## This handle should be changed to the team maintaining the tool
MAINTAINER "Simon Bonsor" scisys.co.uk

ENV DEBIAN-FRONTEND noninteractive

#Try and add those extra packages
COPY packages_required /tmp/packages_required
COPY Rinstallpackages.r /tmp/Rinstallpackages.r
RUN /usr/bin/Rscript /tmp/Rinstallpackages.r
COPY local_packages/* /tmp/
COPY local_packages_required /tmp/packages_required
COPY Rinstalllocalpackages.r /tmp/Rinstalllocalpackages.r
RUN /usr/bin/Rscript /tmp/Rinstalllocalpackages.r

