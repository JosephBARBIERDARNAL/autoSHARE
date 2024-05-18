############################################################
## This script reads all the .dta files in the input directory
## and writes a .csv with one row per variable, containing the
## variable name and its label.
############################################################


library(haven)
library(Hmisc)
library(glue)

get_descriptions <- function(path) {
   data <- read_dta(path)
   names_and_labels <- data.frame(
      NomVariable = names(data),
      Label = sapply(
         names(data),
         function(x) label(data[[x]])
      )
   )
   nom_fichier_csv <- gsub("dta$", "csv", basename(path))
   path_csv <- file.path(output_dir, nom_fichier_csv)
   print(path_csv)
   #write.csv(names_and_labels, path_csv, row.names = FALSE)
}

input_dirs <- paste0("static/data/sharew", 1:9, "_rel9-0-0_ALL_datasets_stata")
output_dir <- "static/columns"
for (input_dir in input_dirs) {
   fichiers_dta <- list.files(path = input_dir, pattern = "\\.dta$", full.names = TRUE)
   sapply(fichiers_dta, get_descriptions)
}
