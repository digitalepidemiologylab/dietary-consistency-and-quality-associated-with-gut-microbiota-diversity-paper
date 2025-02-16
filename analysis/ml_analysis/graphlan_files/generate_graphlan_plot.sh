# Set the path to where Graphlan is installed
#path_to_graphlan="../../graphlan"
path_to_graphlan="/Users/rohansingh/WORK/qiime2_2024/graphlan"

# Run GraphLAN commands using the variable
${path_to_graphlan}/graphlan_annotate.py --annot nutrition_features_annotations.txt nutrition_features_tree.txt nutrition_features_tree_annotated.xml
${path_to_graphlan}/graphlan.py nutrition_features_tree_annotated.xml nutrition_features_importance_plot.png --dpi 300 --size 8