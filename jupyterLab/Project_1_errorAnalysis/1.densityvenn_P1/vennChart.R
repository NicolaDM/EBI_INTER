# # Specify a user directory to install the R package
user_lib <- "~/R/library"
if (!dir.exists(user_lib)) {
  dir.create(user_lib, recursive = TRUE)
}
# Add user directory to library path
.libPaths(user_lib)

packages <- c("ggplot2", "venn", "cowplot", "ggVennDiagram")
new_packages <- packages[!(packages %in% installed.packages(lib.loc = user_lib)[,"Package"])]
if(length(new_packages)) {
  install.packages(new_packages, lib = user_lib, repos = "https://cran.rstudio.com/")
}


library(ggplot2)
library(sf)
library(venn)
library(cowplot)
library(ggVennDiagram)

# Import data for errPOS
data_ERR <- read.table("/nfs/research/goldman/zihao/Code/jupyterLab/A_Datas/ERR_POS_all.txt", header = TRUE, sep = "\t")

x_ERR <- list(
  AF = data_ERR$ID_POS[data_ERR$Flag_AF == "True"],
  SB = data_ERR$ID_POS[data_ERR$Flag_SB == "True"],
  COV = data_ERR$ID_POS[data_ERR$Flag_COV == "True"]
)

x_ERR_F <- list(
  AF = data_ERR$ID_POS[data_ERR$Flag_AF == "False"],
  SB = data_ERR$ID_POS[data_ERR$Flag_SB == "False"],
  COV = data_ERR$ID_POS[data_ERR$Flag_COV == "False"]
)

format_count <- function(count) {
  result <- ifelse(count >= 1e9, paste0(round(count / 1e9, 2), "B"),
                   ifelse(count >= 1e6, paste0(round(count / 1e6, 2), "M"),
                          ifelse(count >= 1e3, paste0(round(count / 1e3, 2), "K"),
                                 as.character(count))))
  return(result)
}

data_err <- process_data(Venn(x_ERR))
data_err_F <- process_data(Venn(x_ERR_F))

data_ERR$Flag_AF <- as.logical(data_ERR$Flag_AF)
data_ERR$Flag_SB <- as.logical(data_ERR$Flag_SB)
data_ERR$Flag_COV <- as.logical(data_ERR$Flag_COV)

data_ERR_F_count <- sum(!data_ERR$Flag_AF & !data_ERR$Flag_SB & !data_ERR$Flag_COV)
data_ERR_count <- sum(data_ERR$Flag_AF & data_ERR$Flag_SB & data_ERR$Flag_COV)

#==================================================
#PLOT FOR ERRPOS
#==================================================
manual_colors <- c("AF" = "#6488AE", "SB" =  "#D9BFCB", "COV" = "#A3AC5D")

final_plot <- plot_grid(
  title,
  ggplot() +
    geom_sf(aes(fill = round(count/nrow(data_ERR)*100, 3)), data = venn_region(data_err)) +
    
    geom_sf(aes(color = name), data = venn_setedge(data_err), show.legend = FALSE, lwd = 1.5) +
    geom_sf_text(aes(label = ifelse(name %in% c("AF", "SB", "COV"), "", name)), data = venn_setlabel(data_err)) +
    geom_sf_label(aes(label = paste0(format_count(count), " (", round(count/nrow(data_ERR)*100, 3), "%)")),
                  data = venn_region(data_err),
                  size = 5) +  theme_void()+ 
    scale_fill_gradientn(colors =
                           c("#F4FAFE","#E2F3FC","#D9EFFB","#ACDEF6","#9AD8F4","#91D4F3","#82C7F8","#6FBEF7","#5CB6F6","#499DF5"), 
                         values = c(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), limits = c(0, 100), guide = "none")+
    scale_color_manual(values = manual_colors)+
    theme(panel.border = element_rect(colour = "grey", fill=NA, size=1), 
          panel.background = element_rect(fill = "#F4FAFE")),
  legend, 
  nrow = 3, 
  rel_heights = c(0.1, 1, 0.1), 
  align = "h", 
  axis = "l"
)

# print(final_plot)

ggsave("Figure\\ERRPOS.png", plot = final_plot, width = 10, height = 10)
print(paste0("Statistics for data not displayed in Venn charts: ", format_count(data_ERR_F_count), " (", round(data_ERR_F_count/nrow(data_ERR)*100, 3), "%)"))

# Import data for allPOS
AF <- 7547094
SB <- 1782985
COV <- 583535685
AF_SB <- 17971522
AF_COV <- 954583
SB_COV <- 253433
ALL <- 377289
ALL_UN <-3420841838
NB_all <- AF+SB+COV+AF_SB+AF_COV+SB_COV+ALL+ALL_UN

data_err@region[["count"]][1] <- AF
data_err@region[["count"]][2] <- SB
data_err@region[["count"]][3] <- COV
data_err@region[["count"]][4] <- AF_SB
data_err@region[["count"]][5] <- AF_COV
data_err@region[["count"]][6] <- SB_COV
data_err@region[["count"]][7] <- ALL


#==================================================
#PLOT FOR ALLPOS
#==================================================
manual_colors <- c("AF" = "#6488AE", "SB" =  "#D9BFCB", "COV" = "#A3AC5D")

final_plot <- plot_grid(
  title,
  ggplot() +
    geom_sf(aes(fill = round(count/NB_all*100, 3)), data = venn_region(data_err)) +
    geom_sf(aes(color = name), data = venn_setedge(data_err), show.legend = FALSE, lwd = 1.5) +
    geom_sf_text(aes(label = ifelse(name %in% c("AF", "SB", "COV"), "", name)), data = venn_setlabel(data_err)) +
    geom_sf_label(aes(label = paste0(format_count(count), " (", round(count/NB_all*100, 3), "%)")),
                  data = venn_region(data_err),
                  size = 5) +  theme_void()+ 
    scale_fill_gradientn(colors =
                           c("#F4FAFE","#E2F3FC","#D9EFFB","#ACDEF6","#9AD8F4","#91D4F3","#82C7F8","#6FBEF7","#5CB6F6","#499DF5"), 
                         values = c(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), limits = c(0, 100), guide = "none")+
    scale_color_manual(values = manual_colors)+
    theme(panel.border = element_rect(colour = "grey", fill=NA, size=1), 
          panel.background = element_rect(fill = "#5CB6F6")),
  legend, 
  nrow = 3, 
  rel_heights = c(0.1, 1, 0.1), 
  align = "h", 
  axis = "l"
)

ggsave("Figure\\ALLPOS.png", plot = final_plot, width = 10, height = 10)
print(paste0("Statistics for data not displayed in Venn charts: ", format_count(ALL_UN), " (", round(ALL_UN/NB_all*100, 3), "%)"))