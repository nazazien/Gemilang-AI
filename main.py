from keperluan_modul import *
bg()

def transpose(matrix):
    return list(map(list, zip(*matrix)))

def matrix_multiplication(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

def matrix_inverse(matrix):
    n = len(matrix)
    identity = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    augmented = [matrix[i] + identity[i] for i in range(n)]

    for i in range(n):
        if augmented[i][i] == 0:
            for j in range(i + 1, n):
                if augmented[j][i] != 0:
                    augmented[i], augmented[j] = augmented[j], augmented[i]
                    break
            else:
                raise ValueError("Matrix is singular.")

        factor = augmented[i][i]
        augmented[i] = [x / factor for x in augmented[i]]

        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [x_j - factor * x_i for x_j, x_i in zip(augmented[j], augmented[i])]

    return [row[n:] for row in augmented]

def prepare_matrices(subset, model_types, transmission_types, fuel_types):
    X = []
    Y = []
    for _, row in subset.iterrows():
        model_features = [1 if row['model'] == model else 0 for model in model_types]
        transmission_features = [1 if row['transmission'] == trans else 0 for trans in transmission_types]
        fuel_features = [1 if row['fuelType'] == fuel else 0 for fuel in fuel_types]

        features = [1, row['mileage'], row['year'], row['engineSize'], row['mpg'], row['tax']]
        features.extend(model_features + transmission_features + fuel_features)
        X.append(features)
        Y.append(row['price'])
    return X, Y

def calculate_weights(X, Y):
    X_T = transpose(X)
    X_T_X = matrix_multiplication(X_T, X)
    X_T_Y = matrix_multiplication(X_T, [[y] for y in Y])

    for i in range(len(X_T_X)):
        X_T_X[i][i] += 1e-5

    X_T_X_inv = matrix_inverse(X_T_X)
    W = matrix_multiplication(X_T_X_inv, X_T_Y)
    return [w[0] for w in W]

def random_forest_subsets(data, num_trees, sample_size=0.5):
    subsets = []
    data_size = len(data)
    sample_count = int(sample_size * data_size)
    for i in range(num_trees):
        subset = data.sample(sample_count, replace=True, random_state=i)
        subsets.append(subset)
    return subsets

def train_random_forest(subsets, model_types, transmission_types, fuel_types):
    forest_weights = []
    for subset in subsets:
        X, Y = matriks.prepare_matrices(subset, model_types, transmission_types, fuel_types)
        weights = calculate_weights(X, Y)
        forest_weights.append(weights)
    return forest_weights

def predict_random_forest(features, forest_weights):
    predictions = [sum(f * w for f, w in zip(features, weights)) for weights in forest_weights]
    return sum(predictions) / len(predictions)

def split_train_test(data, test_ratio=0.2):
    test_size = int(len(data) * test_ratio)
    test_indices = [i for i in range(len(data)) if i % int(1/test_ratio) == 0]
    test_data = data.iloc[test_indices]
    train_data = data.drop(test_data.index)
    return train_data, test_data

page = option_menu(
    menu_title=None,  
    options=["Home", "Estimation", "Rate Us", "About Us"],
    icons=["house","bar-chart","chat","people"],
    menu_icon="cast", 
    default_index=0,
    orientation="horizontal",    
)

if page == "Home":    
    st.snow()    
    st.header(':rainbow[HOME]', divider='rainbow')
    st.markdown("<marquee style='color:#675858;'> 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 Welcome To Gemilang's App 🔥 </marquee>", unsafe_allow_html=True)
    st.title('HOW MUCH IS MY CAR COST?')
    st.write(':grey[Friday, 08 November 2023. By [gemilang.com](http://localhost:8501/%F0%9F%91%A5%20About%20Us)]')      
        
    video_file = open("Documents\profil.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)
    
    st.subheader('Why Choose Gemilang?')
    st.write("Accuracy, convenience, and trust are at the heart of our application. Whether you’re looking to sell your TOYOTA RAV4, Corolla, or any other model, Gemilang ensures a fair price estimate. Join thousands of satisfied users who’ve successfully sold their cars with confidence using Find Your Car Price. Our platform analyzes key factors such as model, year, mileage, and engine size to deliver an accurate valuation in minutes. You no longer have to spend hours researching market trends or consulting multiple sources. With Gemilang, the process is seamless, and you save both time and effort.")
    
    st.subheader('Know the True Value of Your TOYOTA')
    st.write("Gemilang, our application is for those of you who are confused about determining the selling price of a used TOYOTA car quickly and accurately. Check the estimated price of your car carefully before selling your car. Selling a car can be overwhelming, especially when you're unsure of its worth in the current market. Find Your Car Price simplifies this process by providing a precise price estimate tailored to your TOYOTA model. With our cutting-edge tools, you can confidently set a competitive price that reflects your car's actual value.")
              
    
    st.subheader('Promoting Your Used Car')    
    col1,col2,col3 = st.columns([2,2,2])
    with col1:
        st.image(Image.open('Documents/image/1.png'), width=250)
        st.write('Accurate price estimates: Entering the details of the vehicle you want to sell will produce an immediate selling price that matches the market.')

    with col2:
        st.image(Image.open('Documents/image/2.png'), width=250)
        st.write('Save Time: No need to search for prices for a long time, simply entering the car details will produce an accurate price.')

    with col3:
        st.image(Image.open('Documents/image/3.png'), width=250)
        st.write('Right price: Provides benefits for both parties so that no one feels disadvantaged and can compete in the market.')    

elif page == "Estimation":
    st.header(':rainbow[USED CAR PRICE ESTIMATION]', divider='rainbow')
    df = pd.read_csv('Documents/data/toyota.csv')

    model_types = list(df['model'].unique())
    transmission_types = list(df['transmission'].unique())
    fuel_types = list(df['fuelType'].unique())

    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 3, 1])
        with col2:
            st.subheader('Price Estimate Form')

        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            model = st.selectbox('Select Car Model', model_types)
            year = st.number_input('Enter Car Year: ')
            mileage = st.number_input('Enter mileage (km): ')
            tax = st.number_input('Enter Car Tax: ')
        with col2:
            engineSize = st.number_input('Enter Engine Size: ')
            transmission = st.selectbox('Select Transmission Type', transmission_types)
            fuelType = st.selectbox('Select Fuel Type', fuel_types)
            mpg = st.number_input('Enter Car Fuel Consumption: ')

    train_data, test_data = split_train_test(df)
    subsets = random_forest_subsets(train_data, num_trees=10)
    forest_weights = train_random_forest(subsets, model_types, transmission_types, fuel_types)

    user_features = [1, mileage, year, engineSize, mpg, tax]
    user_features.extend([1 if model == m else 0 for m in model_types])
    user_features.extend([1 if transmission == t else 0 for t in transmission_types])
    user_features.extend([1 if fuelType == f else 0 for f in fuel_types])

    estimated_price = predict_random_forest(user_features, forest_weights)
    actual_prices = [row['price'] for _, row in test_data.iterrows()]
    predicted_prices = [
        predict_random_forest(
            [1, row['mileage'], row['year'], row['engineSize'], row['mpg'], row['tax']]
            + [1 if row['model'] == m else 0 for m in model_types]
            + [1 if row['transmission'] == t else 0 for t in transmission_types]
            + [1 if row['fuelType'] == f else 0 for f in fuel_types],
            forest_weights
        )
        for _, row in test_data.iterrows()
    ]

    mse = sum((p - a) ** 2 for p, a in zip(predicted_prices, actual_prices)) / len(actual_prices)
    mape = sum(abs((a - p) / a) for p, a in zip(predicted_prices, actual_prices) if a != 0) / len(actual_prices) * 100

    if estimated_price < 0:
        st.error("Masukkan data yang valid.")
        st.image(Image.open('Documents/image/so.png'), caption='Source: https://storyset.com/')
    else:
        pemanis.sukses()
        st.subheader('', divider='rainbow')
        gambar, hasil = st.columns([2, 2])
        with gambar:
            st.image(Image.open('Documents/image/oe.png'), width=350, caption='Source: https://storyset.com/')
        with hasil:
            st.subheader(':rainbow[ESTIMATED PRICE : ]')
            st.title(f'$ {estimated_price:,.0f}')
            st.write("Model Mean Squared Error (MSE):", mse)
            st.write("Mean Absolute Percentage Error (MAPE): ")
            st.write(round(mape, 2), "%")

            data = {
                'Actual Price': actual_prices,
                'Predicted Price': predicted_prices
            }
            export = pd.DataFrame(data)            
            base_folder = os.path.expanduser("~\\Documents\\data")
            os.makedirs(base_folder, exist_ok=True)
            path = os.path.join(base_folder, "prediksi.xlsx")            
            export.to_excel(path, index=False, engine='openpyxl')
                        
            with open(path, "rb") as file:
                st.download_button(
                    label="📄 Export to Excel",
                    data=file,
                    file_name="prediksi.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.subheader('', divider='rainbow')

elif page == "Rate Us":    
    st.header(':rainbow[RATE US]', divider='rainbow')        

    def save_to_csv(timestamp, rating, feedback):
        rating_map = { "⭐️": 1, "⭐️⭐️": 2, "⭐️⭐️⭐️": 3, "⭐️⭐️⭐️⭐️": 4, "⭐️⭐️⭐️⭐️⭐️": 5 }        
        rating = rating_map.get(rating, 0)

        data = pd.DataFrame({'Timestamp': [timestamp], 'Rating': [rating], 'Ulasan': f"{feedback}"})
        existing_df = pd.read_csv('Documents/data/ulasan.csv')
        data = pd.concat([existing_df, data], ignore_index=True)
        data.to_csv('Documents/data/ulasan.csv', index=False)

    feedback_data = pd.read_csv('Documents/data/ulasan.csv').sort_values(by='Rating', ascending=False)
    rating_counts = feedback_data['Rating'].value_counts().sort_index(ascending=False)
    rating_options = [f"⭐️" * rating + f" {rating_counts.get(rating, 0)}" for rating in range(5, 0, -1)]
    rating_selected = 5 - rating_options.index(st.selectbox("Select Rating", options=rating_options))

    filtered_feedback = feedback_data[feedback_data['Rating'] == rating_selected]
    with st.container(border=True , height=200):
        if filtered_feedback.empty:
            st.write("No feedbacks matching the selected star rating.")
        else:
            for _, row in filtered_feedback.iterrows():
                with st.chat_message("user"):
                    col1, col2 = st.columns([15, 1])
                    with col1:
                        stars = "⭐️" * row['Rating']
                        st.markdown(f"{stars}\n\n`{row['Timestamp']}`")
                    with col2:
                        st.write(f"{row['Rating']}/5")
                    st.write("")
                    st.markdown(row['Ulasan'])
            
    
    st.write("---")
    rating = st.radio("Rating:", options=["⭐️", "⭐️⭐️", "⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️⭐️"], index=3, horizontal=True)
    feedback = st.chat_input("Feedback:")
    if feedback:
        save_to_csv(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rating, feedback)
        st.success('Thank you! Your feedback has been saved.')
        st.balloons()


elif page == "About Us":    
    pemanis.profil()

    st.header(':rainbow[ABOUT US]', divider='rainbow')
    st.subheader('We are behind the scenes of Gemilang!')
    st.subheader("")

    deskripsi, poto = st.columns([3,2])
    with deskripsi:
        st.markdown('''The "Gemilang" team consists of three students from the 2023E Bachelor of Data Science Study Program, Faculty of Mathematics and Natural Sciences, Surabaya State University.
This team was formed with the aim of fulfilling the final project assignment for the third semester in the Artificial Intelligence course under the guidance of Mrs. Dr. Elly Matul Imah, M.Kom.
The project carried out by this team is "A System for Estimating the Price of Used Toyota Cars."
The "Gemilang" team hopes to make a positive contribution in fulfilling the final assignment of this third semester.
''')

    with poto:
        st.image(Image.open('Documents/image/G Logo.png'), width=250)
    st.markdown('''Our Vision
Become a trusted solution for predicting used car prices.
\n
Our Mission
Create an easy-to-use used car price prediction tool.
Help sellers determine the right price.
Increase our knowledge through practical experience.''')
    st.subheader("",divider='grey')
    st.subheader(":rainbow[Our Team]", divider='grey')

    col1,col2,col3 = st.columns([2,2,2])
    with col1:
        st.image(Image.open('Documents/image/naza.jpg'), width=150)
        st.markdown('''Naza Sulthoniyah Wahda
                    23031554026
                    naza.23026@gmail.com''')

    with col2:
        st.image(Image.open('Documents/image/salwa.jpeg'), width=150)
        st.markdown('''Salwa Nadhifah Az Zahrah
                    23031554136
                    salwa.23040@mhs.unesa.ac.id''')

    with col3:
        st.image(Image.open('Documents/image/salsa.jpg'), width=150)
        st.markdown('''Salsabilla Indah Rahmawati
                    23031554193
                    salsabilla.23193@mhs.unesa.ac.id''')

