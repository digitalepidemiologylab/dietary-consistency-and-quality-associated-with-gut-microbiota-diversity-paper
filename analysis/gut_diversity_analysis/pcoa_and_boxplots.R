library(ggplot2)
library(dplyr)
library(forcats)
library(RColorBrewer)
# library(gridExtra)
library(patchwork)

meta <- read.csv("../../data/fay_meta_diets.csv",
                 row.names = 1)
meta$age_group <- as.factor(meta$age_group)
meta$age_group_2 <- factor(meta$age_group_2, levels = c("<35", "35-50", ">50"))
meta$bmi_cat <- factor(meta$bmi_cat, levels=c("Underweight","Normal","Overweight","Obese"))
meta$gender <- as.factor(meta$gender)
meta$language <- as.factor(meta$language)
meta$smoking <- factor(meta$smoking, levels = c("smoker", "former", "non-smoker" ))
meta$swiss_citizen <- factor(meta$swiss_citizen, 
                             levels = c("foreigner", "binational", "swiss"))

#meta <- meta %>% filter(antibiotics_treatment != "")

################################################################################
#########  PCOA PLOT
################################################################################
library(ape)

distance_matrix_path <- "../../qiime/unweighted_unifrac_distance_matrix/distance-matrix.tsv"
beta_dist <- read.table(distance_matrix_path, sep = "\t", header = TRUE, row.names = 1)

beta_dist <- as.dist(beta_dist)
pcoa_results <- pcoa(beta_dist)

pcoa_df <- as.data.frame(pcoa_results$vectors)
pcoa_df$sample.id <- rownames(pcoa_df)

meta$HEI_Quartile <- factor(meta$HEI_Quartile) 
#pcoa_plot_df <- merge(meta, pcoa_df, by = "row.names")
pcoa_plot_df <- merge(pcoa_df, meta, by.y = "sample.id", by.x = "row.names", all.x = FALSE, all.y = TRUE)
print(nrow(pcoa_plot_df))

# Recalculate the medians for plotting
medians <- aggregate(cbind(Axis.1, Axis.2) ~ HEI_Quartile, data = pcoa_plot_df, FUN = median)

##########################
p3 <- ggplot(pcoa_plot_df, aes(x = Axis.1, y = Axis.2, color = HEI_Quartile)) +
  geom_point() +
  stat_ellipse(aes(fill = HEI_Quartile), geom = "polygon", alpha = 0.15, linetype = 3) +
  scale_color_brewer(type = "div", palette = "Spectral") +
  scale_fill_brewer(type = "div", palette = "Spectral") +
  geom_point(data = medians, aes(x = Axis.1, y = Axis.2, fill = HEI_Quartile), 
             size = 3, shape = 21, color = "black", stroke = 0.5) +
  theme_minimal() +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_blank(),
    axis.line.x = element_line(color = "black", size = 0.25),
    axis.line.y = element_line(color = "black", size = 0.25),
    # Increase axis label size to 12 (title)
    axis.title.x = element_text(face="bold", colour = "black", size = 12),
    axis.title.y = element_text(face="bold", colour = "black", size = 12),
    # Increase tick label size to 10
    axis.text.x = element_text(colour = "black", size = 10),
    axis.text.y = element_text(colour = "black", size = 10),
    axis.ticks = element_line(color = "black"),
    panel.border = element_blank(),
    # Panel label settings
    plot.tag = element_text(
      face = "bold",
      size = 21,
      #margin = margin(b = 10, l = 10)
    ),
    plot.tag.position = c(0.02, 0.98)
  ) +
  labs(
    x = paste0("PCoA 1 (", 100 * round(pcoa_results$values$Relative_eig[1], 4), "%)"),
    y = paste0("PCoA 2 (", 100 * round(pcoa_results$values$Relative_eig[2], 4), "%)"),
    tag = "D"
  )

ggsave(filename = "../../figures/gut_diversity_analysis/pcoa_HEI_quartiles.png", plot = p3, width = 6.1, height = 5, dpi = 300, units = "in")

##############################################################################
########################## BOXPLOT STATS
##############################################################################
library(ggplot2)
library(ggstatsplot)
library(ggsignif)
library(tidyverse)
library(viridis)

create_ggbetweenstats_plot <- function(data, x_var, y_var, show_subtitle = TRUE, 
                                       show_centrality = TRUE, type = "np", 
                                       p_adjust_method = "fdr",
                                       asterisk_pos_start = 5,
                                       asterisk_pos_step = 1,
                                       break_seq = c(4, 8.5, 1),
                                       package = "ggsci",
                                       palette = "default_jama") {
  # Convert strings to symbols for ggbetweenstats
  x_sym <- rlang::ensym(x_var)
  y_sym <- rlang::ensym(y_var)
  
  # Call ggbetweenstats with provided parameters, ensure your library is correctly loaded
  plot <- ggstatsplot::ggbetweenstats(
    data = data, 
    x = {{ x_sym }},
    y = {{ y_sym }},
    type = type,
    p.adjust.method = p_adjust_method,
    pairwise.comparisons = TRUE,
    pairwise.display = "none", #"significant",
    messages = FALSE,  # Set to TRUE if you want informative messages
    # package = package,
    # palette = palette,
    results.subtitle = show_subtitle,
    centrality.plotting = show_centrality,
    centrality.point.args = list(alpha=0),
    #centrality.point.args = list(size = 3, color = "darkred"),
    centrality.label.args = list(alpha=0),
    # centrality.label.args = list(alpha=0, size = 2, nudge_x = 0.4, segment.linetype = 4, min.segment.length = 0),
    ggplot.component = list(
      ggplot2::scale_y_continuous(breaks = seq(break_seq[1], break_seq[2], break_seq[3]), 
                                  limits = c(break_seq[1], break_seq[2])),
      ggplot2::theme(
        axis.line.x = element_line(color = "black"),
        axis.line.y = element_line(color = "black"),
        panel.grid.major = element_blank(),  
        panel.grid.minor = element_blank(),  
        axis.ticks = element_line(color = "black"),
        axis.text.x = element_text(size = 9),  # Set x-axis tick label size
        axis.text.y = element_text(size = 9),  # Set y-axis tick label size
        axis.title.x = element_text(size = 10),  # Set x-axis title size
        axis.title.y = element_text(size = 10),  # Set y-axis title size
        axis.text.y.right = element_blank(),
        axis.ticks.y.right = element_blank(), 
        axis.title.y.right = element_blank()
      ) 
    ),
    #violin.args = list(width = 0, linewidth = 0),
    point.args = list(alpha = 0),
    boxplot.args = list(width = 0.3, fill=palette, alpha=0.7),
  )
  
  df <- pairwise_comparisons(data, {{ x_sym }}, {{ y_sym }}, 
                             type = ifelse(type == "p", "parametric", "nonparametric"), 
                             p.adjust.method = "fdr") %>%
    dplyr::mutate(groups = purrr::pmap(.l = list(group1, group2), .f = c)) %>%
    dplyr::arrange(group1) %>%
    dplyr::mutate(
      asterisk_label = case_when(
        p.value < 0.001 ~ "***",
        p.value < 0.01 ~ "**",
        p.value < 0.05 ~ "*",
        TRUE ~ NA_character_  # Assign NA for non-significant results
      )
    ) %>%
    dplyr::filter(!is.na(asterisk_label))
  
  print(df)
  
  if(dim(df)[1] == 0){
    return(plot)
  }
  
  astersisk_pos = seq(from = asterisk_pos_start, by = asterisk_pos_step, 
                      length.out = dim(df)[1])
  plot <- plot +
    ggsignif::geom_signif(
      comparisons = df$groups,
      map_signif_level = TRUE,
      annotations = df$asterisk_label,
      y_position = astersisk_pos,
      test = NULL,
      na.rm = TRUE,
      textsize = 5,
    )
  
  return(plot)
}

################################################################################

show_subtitle = FALSE
show_centrality = TRUE
boxplot_save_width = 3
boxplot_save_height = 4

p4 <- create_ggbetweenstats_plot(data = meta, x_var = "age_group_2", y_var = "HEI",
                           show_subtitle = show_subtitle, show_centrality = show_centrality, 
                           type = "p", asterisk_pos_start = 80, asterisk_pos_step = 6,
                           break_seq = c(30, 100, 15),
                           palette = c("gold","orange","brown"))
p4 <- p4 + labs(x = "Age", y="HEI Score")

p5 <- create_ggbetweenstats_plot(data = meta, x_var = "smoking", y_var = "HEI",
                                 show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                 type = "p", asterisk_pos_start = 80, asterisk_pos_step = 6,
                                 break_seq = c(30, 95, 15),
                                 palette = c("grey","blue","cyan"))
p5 <- p5 + labs(x = "Smoking", y="HEI Score")

p6 <- create_ggbetweenstats_plot(data = meta, x_var = "bmi_cat", y_var = "HEI",
                                 show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                 type = "p", asterisk_pos_start = 80, asterisk_pos_step = 6,
                                 break_seq = c(30, 100, 15),
                                 palette = c("darkgreen","#8DB600","lightgreen","#9EFD38"))
p6 <- p6 + labs(x = "BMI", y="HEI Score")

p7 <- create_ggbetweenstats_plot(data = meta, x_var = "age_group_2", y_var = "shannon_entropy",
                                 show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                 type = "np", asterisk_pos_start = 7.5, asterisk_pos_step = 0.5,
                                 break_seq = c(4, 9, 1),
                                 palette = c("gold","orange","brown"))
p7 <- p7 + labs(x = "Age", y="Shannon Diversity")

p8 <- create_ggbetweenstats_plot(data = meta, x_var = "smoking", y_var = "shannon_entropy",
                                 show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                 type = "np", asterisk_pos_start = 8, asterisk_pos_step = 0.5,
                                 break_seq = c(4, 10, 1),
                                 palette = c("grey","blue","cyan"))
p8 <- p8 + labs(x = "Smoking", y="Shannon Diversity")

p9 <- create_ggbetweenstats_plot(data = meta, x_var = "bmi_cat", y_var = "shannon_entropy",
                                 show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                 type = "np", asterisk_pos_start = 7.8, asterisk_pos_step = 0.5,
                                 break_seq = c(4, 9, 1),
                                 palette = c("darkgreen","#8DB600","lightgreen","#9EFD38"))
p9 <- p9 + labs(x = "BMI", y="Shannon Diversity")

# p10 <- create_ggbetweenstats_plot(data = meta, x_var = "general_hunger_level", y_var = "HEI",
#                                  show_subtitle = show_subtitle, show_centrality = show_centrality, 
#                                  type = "p", asterisk_pos_start = 80, asterisk_pos_step = 5,
#                                  break_seq = c(30, 80, 15),
#                                  palette = c("pink","#B43757","#FF2400","#7C0A02","#420D09"))
# 
# p11 <- create_ggbetweenstats_plot(data = meta, x_var = "general_hunger_level", y_var = "shannon_entropy",
#                                  show_subtitle = show_subtitle, show_centrality = show_centrality, 
#                                  type = "np", asterisk_pos_start = 8, asterisk_pos_step = 0.5,
#                                  break_seq = c(4, 9, 1),
#                                  palette = c("pink","#B43757","#FF2400","#7C0A02","#420D09"))

p10 <- create_ggbetweenstats_plot(data = meta, x_var = "stress_level", y_var = "HEI",
                                  show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                  type = "p", asterisk_pos_start = 80, asterisk_pos_step = 5,
                                  break_seq = c(30, 100, 15),
                                  palette = c("pink","#B43757","#FF2400","#7C0A02","#420D09"))
p10 <- p10 + labs(x = "Stress Level", y="HEI Score")

p11 <- create_ggbetweenstats_plot(data = meta, x_var = "stress_level", y_var = "shannon_entropy",
                                  show_subtitle = show_subtitle, show_centrality = show_centrality, 
                                  type = "np", asterisk_pos_start = 700, asterisk_pos_step = 75,
                                  break_seq = c(0, 900, 200),
                                  palette = c("pink","#B43757","#FF2400","#7C0A02","#420D09"))
p11 <- p11 + labs(x = "Stress Level", y="Shannon Diversity")

############## Save Figures Individually
# plot_list <- list(p4 = p4, p5 = p5, p6 = p6, p7 = p7, p8 = p8, p9 = p9)
# save_path <- "./ggStatsBoxplots"
# 
# for (plot_name in names(plot_list)) {
#   ggsave(
#     filename = paste0(save_path, "/", plot_name, ".png"),
#     plot = plot_list[[plot_name]], 
#     width = boxplot_save_width, 
#     height = boxplot_save_height, 
#     dpi = 300, 
#     units = "in"
#   )
# }
############## 

# p <- ggbetweenstats(data = meta, x = bmi_cat, y = shannon_entropy, pairwise.display = "none")
# 
# pairwise_comparisons(meta, bmi_cat, shannon_entropy) %>%
#   dplyr::mutate(groups = purrr::pmap(.l = list(group1, group2), .f = c)) %>%
#   dplyr::arrange(group1) %>%
#   dplyr::mutate(asterisk_label = c("**", "***", "**"))


##############################################################################
########################## COMBINING PLOTS
##############################################################################

########################## 

# Combine plots with desired layout
p_boxplots <- (
  (p4 | p5 | p6 ) / 
    (p7 | p8 | p9 )
) + 
  plot_annotation(
    tag_levels = list(c("E", "F", "G", "H", "I", "J")),
    tag_prefix = '',
    tag_suffix = '',
  )

ggsave(filename = "../../figures/gut_diversity_analysis/figure1_boxplots.png", plot = p_boxplots, width = 11, height = 7, dpi = 300, units = "in")


# # Combine plots with desired layout
# p_boxplots <- (
#   (p4 | p5 | p6 ) / 
#   (p7 | p8 | p9 ) ) + 
#   plot_annotation(tag_levels = 'A',
#                   tag_prefix = '',
#                   tag_suffix = '') +
#   theme(
#     #plot.tag = element_text(face = "bold", size = 21)  # Adjust size as needed
#   )
# ggsave(filename = "figure1_boxplots.png", plot = p_boxplots, width = 11, height = 7, dpi = 300, units = "in")


