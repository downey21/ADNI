
# -*- coding: utf-8 -*-

rm(list = ls())

# install.packages("Hmisc")
# install.packages("./R/ADNIMERGE/IDA_ADNI/ADNIMERGE_0.0.1.tar.gz", repos = NULL, type = "source")

library(Hmisc)
library(ADNIMERGE)

# help(package = "ADNIMERGE")

data(adnimerge, package = "ADNIMERGE")

head(adnimerge)
dim(adnimerge)
str(adnimerge)
# View(adnimerge)

colnames(adnimerge)
