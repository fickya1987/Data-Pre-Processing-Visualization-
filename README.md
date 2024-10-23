1. Streamlit Framework and Setup
- streamlit: A powerful Python framework used to build interactive web applications quickly and easily.
- Page configuration: 
  ```python
  st.set_page_config(page_title="📊 6a.py - Advanced Data Preprocessing App", 
                     page_icon="📊", layout="wide")
  ```
  This sets the app’s title, icon, and layout to provide a good user experience.

---
2. Handling Missing Values 
```python
def handle_missing_values(data):
    ...
```
- Concept: Missing values can skew analysis, so filling them with meaningful values ensures consistency.
- Numeric Columns: Filled with the mean of the column.
- Categorical Columns: Filled with the mode (most frequent value).

---

3. Moving Average Smoothing
```python
def custom_moving_average(data, window_size):
    ...
```
- Concept: Moving averages are used to smooth noisy data to observe trends over time.
- How It Works: Uses a rolling window to average values, creating smoother data curves.

Visualization Example:  
- A line graph is plotted for each numeric column to show the smoothed data.

---

4. Min-Max Normalization with User Input
```python
def custom_min_max_normalization(data, min_value, max_value):
    ...
```
- Concept: Min-Max Normalization scales all data between a user-defined min and max (commonly 0 and 1).
- How It Works:  
   For each numeric column:  
   \[ \text{Normalized Value} = \frac{(x - \text{min\_value})}{(\text{max\_value} - \text{min\_value})} \]
- User Interaction: Users input the min and max values, and the normalized data and plots update in real time.

Why It’s Useful:  
- Ensures that all features are on the same scale, which improves performance for certain models like Naive Bayes.

---

5. Pearson Correlation Matrix
```python
def custom_pearson_correlation(data):
    ...
```
- Concept: Measures the linear correlation between pairs of variables.
  \[ \text{Correlation Coefficient} \in [-1, 1] \]  
- Visualization: A heatmap shows correlations between variables to help identify relationships.

---

6. Chi-Square Test for Categorical Data
```python
def custom_chi_square_test(data, col1, col2):
    ...
```
- Concept: The Chi-Square Test checks if two categorical variables are independent.
- Contingency Table: Summarizes the relationship between two categorical variables.
- Chi-Square Statistic:
  \[ \chi^2 = \sum \frac{(O - E)^2}{E} \]  
  Where \(O\) is the observed frequency, and \(E\) is the expected frequency.
Application:  
- Identifies dependencies between two categorical variables.

---

7. Boundary-Based Binning with User Input
```python
def boundary_binning(data, col, boundaries):
    ...
```
- Concept: Binning divides continuous data into discrete groups or ranges (bins).
- How It Works:  
  Users enter custom boundaries to create bins:
  - Example: Bins = [0, 10, 20, 30] divides data into ranges like [0–10), [10–20), etc.

Use Case: Binning helps simplify continuous data for better visualization or statistical analysis.

---

8. Interactive Visualizations with Plotly
- Plotly provides interactive graphs (line plots, bar charts, heatmaps, and tables).
- Usage in Code:
  ```python
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=smoothed_df.index, y=smoothed_df[col], mode='lines'))
  st.plotly_chart(fig)
  ```
  The above code plots smoothed data, and similar approaches are used for other visualizations.

---
9. User Interface (UI) with Streamlit
- File Uploader: Allows the user to upload a CSV file and displays its preview.
  ```python
  uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
  ```
- Interactive Elements: Users control parameters (like window size, min-max normalization, bin boundaries) through sliders, inputs, and dropdowns. As the user updates the input, the output and visualizations update in real-time.

Why This Approach Works:  
- Checkboxes and Selectboxes control which visualizations are shown, ensuring a clean interface.

---

10. How the App Works:
1. Upload CSV: The user uploads a dataset.
2. reprocessing:  
   - Handles missing values.
   - Allows the user to normalize, smooth, or bin the data interactively.
3. Visualize Data:  
   - Plots smoothed data lines.
   - Creates heatmaps, bar charts, and tables based on user input.
4. Chi-Square Test:  
   - Checks dependencies between two categorical columns.

---

Summary:
This data preprocessing app enables:
- Real-time interaction: The output updates as the user adjusts the input parameters.
- Custom control over data normalization and binning through user input.
- Visualizations for easier interpretation, including smoothed data plots, heatmaps, and chi-square contingency tables.

This version ensures that users have full control over how the data is processed, visualized, and interpreted, making it a versatile tool for data analysis and exploration.
