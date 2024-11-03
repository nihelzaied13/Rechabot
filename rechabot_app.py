import streamlit as st
import pandas as pd

# Load datasets (update the paths to your local dataset files)
movies_df = pd.read_csv("C:/Users/Nihel ZAIED/Documents/rechabot1.2/data/netflix_titles.csv").sample(n=5000, random_state=1)
music_df = pd.read_csv("C:/Users/Nihel ZAIED/Documents/rechabot1.2/data/top_10000_1950-now (1).csv").sample(n=5000, random_state=1)
books_df = pd.read_csv("C:/Users/Nihel ZAIED/Documents/rechabot1.2/data/BooksDataset.csv").sample(n=5000, random_state=1)

# Display column names to debug and confirm
st.write("Movies dataset columns:", movies_df.columns)
st.write("Music dataset columns:", music_df.columns)
st.write("Books dataset columns:", books_df.columns)

# Define function to match expected column names
def get_column_names(df, expected_columns):
    """Helper function to map expected columns to actual dataset columns."""
    actual_columns = {}
    for col in expected_columns:
        if col in df.columns:
            actual_columns[col] = col
        else:
            # Attempt to find close matches if column names differ
            for real_col in df.columns:
                if col.lower() in real_col.lower():  # Case-insensitive match
                    actual_columns[col] = real_col
                    break
    return actual_columns

# Expected columns for each dataset
movie_columns = get_column_names(movies_df, ["title", "description", "rating", "year", "cast", "director", "listed_in"])
music_columns = get_column_names(music_df, ["Track Name", "Artist Name(s)", "Album Name", "Popularity", "Album Release Date"])
book_columns = get_column_names(books_df, ["Title", "Authors", "Description", "Category", "Price"])

# Strip spaces in books dataset to avoid mismatches
books_df[book_columns['Authors']] = books_df[book_columns['Authors']].str.strip()

# Diagnostic: Display unique authors to check data format
st.write("Unique authors in Books dataset:", books_df[book_columns['Authors']].unique())

# Function to generate recommendations based on category and input
def recommend_content(category, input_data, criteria):
    recommendations = pd.DataFrame()  # Empty by default
    if category == "Movies":
        if criteria == "Category":
            recommendations = movies_df[movies_df[movie_columns['listed_in']].str.contains(input_data, case=False, na=False)].head(5)
        elif criteria == "Actor":
            recommendations = movies_df[movies_df[movie_columns['cast']].str.contains(input_data, case=False, na=False)].head(5)
        elif criteria == "Director":
            recommendations = movies_df[movies_df[movie_columns['director']].str.contains(input_data, case=False, na=False)].head(5)
    elif category == "Music":
        if criteria == "Artist":
            recommendations = music_df[music_df[music_columns['Artist Name(s)']].str.contains(input_data, case=False, na=False)].head(5)
    elif category == "Books":
        if criteria == "Author":
            recommendations = books_df[books_df[book_columns['Authors']].str.contains(input_data, case=False, na=False)].head(5)
        elif criteria == "Category":
            recommendations = books_df[books_df[book_columns['Category']].str.contains(input_data, case=False, na=False)].head(5)
    return recommendations

# Streamlit App Interface
st.title("Rechabot - Your Entertainment Recommendation Assistant")

st.sidebar.header("Tell Rechabot What You're Looking For")
# Sidebar for User Input
category = st.sidebar.selectbox("Choose a category", ["Movies", "Music", "Books"])
criteria = None

# Set criteria options based on selected category
if category == "Movies":
    criteria = st.sidebar.selectbox("Search by", ["Category", "Actor", "Director"])
elif category == "Music":
    criteria = st.sidebar.selectbox("Search by", ["Category", "Artist"])
elif category == "Books":
    criteria = st.sidebar.selectbox("Search by", ["Author", "Category"])

input_data = st.sidebar.text_input(f"Enter {criteria}")

# Generate and display recommendations
if st.sidebar.button("Get Recommendations"):
    if input_data:
        recommendations = recommend_content(category, input_data, criteria)
        
        # Determine which columns to display based on availability
        if not recommendations.empty:
            if category == "Movies":
                display_columns = [movie_columns.get('title'), movie_columns.get('description'), movie_columns.get('rating'), movie_columns.get('release_year')]
                display_columns = [col for col in display_columns if col is not None]  # Exclude None entries
                st.write(f"Top recommendations for {category} ({criteria}):")
                st.table(recommendations[display_columns])
            elif category == "Music":
                display_columns = [music_columns.get('Track Name'), music_columns.get('Album Name'), music_columns.get('Popularity'), music_columns.get('Album Release Date')]
                display_columns = [col for col in display_columns if col is not None]
                st.write(f"Top recommendations for {category} ({criteria}):")
                st.table(recommendations[display_columns])
            elif category == "Books":
                display_columns = [book_columns.get('Title'), book_columns.get('Description'), book_columns.get('Price')]
                display_columns = [col for col in display_columns if col is not None]
                st.write(f"Top recommendations for {category} ({criteria}):")
                st.table(recommendations[display_columns])
        else:
            st.write("No recommendations found. Try using different keywords.")
    else:
        st.write("Please enter some preferences to get recommendations.")
