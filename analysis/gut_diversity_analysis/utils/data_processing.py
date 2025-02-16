def process_string(
    s,
    ignore_vars=[
        "PDI_Quintile",
        "hPDI_Quintile",
        "HEI",
        "BMI",
    ],
    newLineSep=3,
):
    if s in ignore_vars:
        return s
    if s == "defecate_quantity_per_day":
        return "Defecation Frequency"
    s = s.replace("_fg", "")
    # Step 1 & 2: Split the string by "_" and replace "_" with a space, then capitalize the first letter
    parts = s.replace("_eaten", "").split("_")
    # capitalized_parts = [part.capitalize() for part in parts]
    capitalized_parts = [part[0].upper() + part[1:] if part else "" for part in parts]

    # Step 3: If there are more than 3 items, insert "\n" in the middle
    if newLineSep and len(capitalized_parts) > newLineSep and "CV" not in s:
        mid_index = len(capitalized_parts) // 2
        processed_string = (
            " ".join(capitalized_parts[:mid_index])
            + "\n"
            + " ".join(capitalized_parts[mid_index:])
        )
    elif "CV" in s:
        processed_string = (
            capitalized_parts[0] + " (" + " ".join(capitalized_parts[1:]) + ")"
        )
    else:
        processed_string = " ".join(capitalized_parts)

    return processed_string
