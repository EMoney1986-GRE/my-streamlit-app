import pandas as pd
import streamlit as st

# Load the dataset
file_path = "extrapolated_dataset.csv"  # Dataset is in the same folder as this script
data = pd.read_csv(file_path)

# Step 1: Filter rows where Original is TRUE
original_data = data[data["Original"] == True]

# Step 2: Create a pivot table for displaying Capacity
pivot_table = original_data.pivot_table(
    index=["Location", "Building Short Name", "Floor #"],
    columns=["Fiscal Year", "Std_or_AWP"],
    values="Capacity",
    aggfunc="first"
)

# Streamlit App Title
st.title("Interactive Capacity Table")

# Display the original pivot table
st.write("Original Capacity Table:")
st.dataframe(pivot_table)

# Step 3: Allow users to interactively edit capacity values
st.write("Modify Capacity Values:")

# Create a copy of the original data to store updated capacities
updated_data = original_data.copy()

for idx, row in original_data.iterrows():
    # Get the range of capacities for this row based on rows where Original = FALSE
    range_data = data[
        (data["Location"] == row["Location"]) &
        (data["Building Short Name"] == row["Building Short Name"]) &
        (data["Floor #"] == row["Floor #"]) &
        (data["Fiscal Year"] == row["Fiscal Year"]) &
        (data["Std_or_AWP"] == row["Std_or_AWP"]) &
        (data["Original"] == False)
    ]["Capacity"]

    min_capacity = range_data.min() if not range_data.empty else 0
    max_capacity = range_data.max() if not range_data.empty else int(row["Capacity"])

    # Create a slider for modifying capacity
    new_capacity = st.slider(
        f"{row['Location']} - {row['Building Short Name']} - {row['Floor #']} - {row['Fiscal Year']} - {row['Std_or_AWP']}",
        min_value=int(min_capacity),
        max_value=int(max_capacity),
        value=int(row["Capacity"])
    )

    # Update the capacity value in the dataset
    updated_data.loc[idx, "Capacity"] = new_capacity

# Step 4: Display the updated pivot table
updated_pivot_table = updated_data.pivot_table(
    index=["Location", "Building Short Name", "Floor #"],
    columns=["Fiscal Year", "Std_or_AWP"],
    values="Capacity",
    aggfunc="first"
)

st.write("Updated Capacity Table:")
st.dataframe(updated_pivot_table)

# Step 5: Save the updated data to a new CSV file
if st.button("Save Changes"):
    updated_data.to_csv("updated_dataset.csv", index=False)
    st.success("Changes saved to updated_dataset.csv")
