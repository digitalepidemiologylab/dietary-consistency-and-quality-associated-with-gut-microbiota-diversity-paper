library(ggplot2)
library(sjPlot)
theme_set(theme_sjplot())
# Read the CSV file
data <- read.csv("../../data/fay_meta_diets.csv")
head(data)

# Set the reference level for age_group_2, gender, and bmi_cat to match the Python model
data$age_group_2 <- factor(data$age_group_2, levels = c("<35", "35-50", ">50"))
data$gender <- relevel(factor(data$gender), ref = "male")
data$smoking <- relevel(factor(data$smoking), ref = "non-smoker")
data$bmi_cat <- relevel(factor(data$bmi_cat), ref = "Normal")
data$antibiotics_treatment <- relevel(factor(data$antibiotics_treatment), ref = TRUE)
data$language <- relevel(factor(data$language), ref = "german")
data$swiss_citizen <- relevel(factor(data$swiss_citizen), ref = "foreign")

triple_interaction_model <- lm(shannon_entropy ~  HEI * gender * age_group_2 + bmi_cat + smoking + eaten_quantity_in_gram + general_hunger_level + defecate_quantity_per_day, data = data) #+ antibiotics_treatment + swiss_citizen + stress_level 
summary(triple_interaction_model)

# Modify the age group levels to include "Age" prefix
data$age_group_2 <- factor(data$age_group_2, 
                           levels = c("<35", "35-50", ">50"),
                           labels = c("Age <35", "Age 35-50", "Age >50"))

# Fit the model with updated factor levels
triple_interaction_model <- lm(shannon_entropy ~ HEI * gender * age_group_2 + 
                                 bmi_cat + eaten_quantity_in_gram + 
                                 general_hunger_level + defecate_quantity_per_day, 
                               data = data)

# Create the base plot with custom colors
p <- plot_model(triple_interaction_model, 
                type = "pred", 
                terms = c("HEI", "gender", "age_group_2"), 
                axis.title = c("HEI Score", "Shannon Entropy"),
                legend.title = "Gender") +
  # Add custom colors for gender
  scale_color_manual(values = c("male" = "blue", "female" = "magenta")) +
  theme(
    # Remove all grid lines
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    
    # Style axis labels
    axis.title.x = element_text(size = 12, face = "bold", colour = "black"),
    axis.title.y = element_text(size = 12, face = "bold", colour = "black"),
    
    # Style axis text
    axis.text.x = element_text(size = 10, colour = "black"),
    axis.text.y = element_text(size = 10, colour = "black"),
    
    # Add panel tag
    plot.tag = element_text(face = "bold", size = 18),
    plot.tag.position = c(0.02, 0.98),
    
    # Remove plot title
    plot.title = element_blank(),
    
    # Style axis lines and ticks
    axis.line = element_line(color = "black", size = 0.25),
    axis.ticks = element_line(color = "black", size = 0.25),
    axis.ticks.length = unit(0.2, "cm"),
    
    # Clean up legend
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 9),
    
    # Style group labels if any
    strip.text = element_text(size = 10, face = "bold"),
    strip.background = element_rect(fill = "white")
  ) +
  labs(tag = "C")

# Save the plot
ggsave("../../figures/gut_diversity_analysis/effects_model_HEI_age_shannon.png", 
       plot = p, 
       width = 7, 
       height = 4.5, 
       dpi = 300)

####################################################################################################
no_interaction_model <- lm(shannon_entropy ~  HEI + gender +  bmi + age + smoking + eaten_quantity_in_gram + general_hunger_level + defecate_quantity_per_day, data = data)
summary(no_interaction_model)

####################################################################################################
no_interaction_model_dailyHEI <- lm(shannon_entropy ~  daily_HEI + gender +  bmi + age + smoking + eaten_quantity_in_gram + general_hunger_level + defecate_quantity_per_day, data = data)
summary(no_interaction_model_dailyHEI)
####################################################################################################