import sys
import json
import random
import googlemaps
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QComboBox, QSlider, QPushButton, QTextEdit,
    QScrollArea, QFrame, QMainWindow
)
from PySide6.QtWebEngineWidgets import QWebEngineView

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyCRHFRwTKaJkSJdUDSR9tIXb3iquFrfVSE')
# Initialize Ollama client

class StarLabel(QLabel):
    def __init__(self, index, callback):
        super().__init__("☆")
        self.index = index
        self.callback = callback
        self.setStyleSheet("font-size: 36px; color: #999;")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedWidth(50)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.callback(self.index)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("InsightMap")
window.setWindowIcon(QIcon('map.ico'))
window.setStyleSheet("""
    QWidget {
        background-color: #ffffff;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 16px;
    }

    QLabel {
        color: #212529;
        font-size: 20px;
        margin: 8px 0;
    }

    QComboBox {
        background-color: #ffffff;
        color: #212529;
        border: 1px solid #ced4da;
        border-radius: 6px;
        padding: 8px;
        font-size: 17px;
        min-height: 36px;
    }

    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #212529;
        border: 1px solid #dee2e6;
    }

    QComboBox:hover, QComboBox:focus {
        border: 1px solid #339af0;
    }

    QSlider::groove:horizontal {
    background: #dee2e6;
    height: 6px;
    border-radius: 3px;
    }

    QSlider::sub-page:horizontal {
        background: #339af0;  /* Blue filled part */
        height: 6px;
        border-radius: 3px;
    }

    QSlider::add-page:horizontal {
        background: #dee2e6;  /* Grey remaining part */
        height: 6px;
        border-radius: 3px;
    }

    QSlider::handle:horizontal {
        background: #339af0;
        border: none;
        height: 16px;
        width: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }

    QPushButton {
        background-color: #339af0;
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        padding: 10px;
        border: none;
        border-radius: 8px;
        margin-top: 24px;
    }

    QPushButton:hover {
        background-color: #1c7ed6;
    }

    QTextEdit {
        color: black;
        font-size: 17px;
        border: 1px solid #000000;
        border-radius: 6px;
        padding: 8px;
        background-color: #ffffff;
    }

    QTextEdit:hover {
        background:rgb(239, 239, 239);
        color:rgb(0, 0, 0);
    }

    QScrollBar:vertical {
        border: none;
        background: #f1f3f5;
        width: 12px;
        margin: 0px;
    }

    QScrollBar::handle:vertical {
        background: #339af0;
        border-radius: 6px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background: #1c7ed6;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
""")

main_layout = QHBoxLayout()

# ----------- FORM LAYOUT -----------
form_widget = QWidget()
form_layout = QVBoxLayout(form_widget)
form_layout.setSpacing(14)
form_layout.setContentsMargins(40, 40, 20, 40)

# ----------- ADDRESS FIELD -----------
address_label = QLabel("📍 Address or Location (Address, City):")
form_layout.addWidget(address_label)
address_box = QTextEdit()
address_box.setMinimumHeight(60)
form_layout.addWidget(address_box)

# ----------- SERVICE TYPE -----------
type_label = QLabel("🌎 Type of Service")
form_layout.addWidget(type_label)

type_combo = QComboBox()
type_combo.addItem("Select a service type")
type_combo.setItemData(0, 0, Qt.UserRole - 1)
type_combo.addItems(["Restaurants", "Hotels", "Auto Services", "Personal Care"])
form_layout.addWidget(type_combo)

sub_label = QLabel("Select a Category")
form_layout.addWidget(sub_label)

subtype_combo = QComboBox()
form_layout.addWidget(subtype_combo)

# ----------- RATING -----------
rating_label = QLabel("★ Minimum Star Rating")
form_layout.addWidget(rating_label)

star_layout = QHBoxLayout()
stars = []
selected_rating = [0]

def on_star_clicked(rating):
    selected_rating[0] = rating
    for i, star in enumerate(stars):
        if i < rating:
            star.setText("★")
            star.setStyleSheet("font-size: 36px; color: #f08c00;")
        else:
            star.setText("☆")
            star.setStyleSheet("font-size: 36px; color: #999;")

for i in range(5):
    star = StarLabel(i + 1, on_star_clicked)
    stars.append(star)
    star_layout.addWidget(star)
form_layout.addLayout(star_layout)

# ----------- DISTANCE -----------
distance_label = QLabel("Maximum Distance: 1 km")
form_layout.addWidget(distance_label)

distance_slider = QSlider(Qt.Orientation.Horizontal)
distance_slider.setRange(1, 50)
distance_slider.setValue(1)
form_layout.addWidget(distance_slider)

# ----------- PRICE RANGE -----------
price_min_label = QLabel("Minimum Price Level")
form_layout.addWidget(price_min_label)

price_min_combo = QComboBox()
price_min_combo.addItems([
    "$ - Inexpensive", "$$ - Moderate", "$$$ - Expensive", "$$$$ - Very Expensive"
])
form_layout.addWidget(price_min_combo)

price_max_label = QLabel("Maximum Price Level")
form_layout.addWidget(price_max_label)

price_max_combo = QComboBox()
price_max_combo.addItems([
    "$ - Inexpensive", "$$ - Moderate", "$$$ - Expensive", "$$$$ - Very Expensive"
])
form_layout.addWidget(price_max_combo)

def on_price_min_changed(index):
    if index > price_max_combo.currentIndex():
        price_max_combo.setCurrentIndex(index)

def on_price_max_changed(index):
    if index < price_min_combo.currentIndex():
        price_min_combo.setCurrentIndex(index)

price_min_combo.currentIndexChanged.connect(on_price_min_changed)
price_max_combo.currentIndexChanged.connect(on_price_max_changed)

# ----------- COMMENTS -----------
search_button = QPushButton("🔍 Search Now")
form_layout.addWidget(search_button)

# ----------- SCROLL AREA -----------
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setWidget(form_widget)
scroll_area.setFrameShape(QFrame.NoFrame)

# ----------- MAP VIEW -----------
map_view = QWebEngineView()
map_view.setMinimumSize(600, 400)

# ----------- FINAL LAYOUT -----------
main_layout.addWidget(scroll_area, 2)
main_layout.addWidget(map_view, 3)
window.setLayout(main_layout)

# ----------- LOGIC -----------
sub_options = {
    "Restaurants": ["Italian", "BBQ", "Vegan", "Fast Food", "Mexican", "Chinese", "Desserts"],
    "Hotels": ["Budget", "Luxury", "Spa"],
    "Auto Services": ["Repair", "Maintenance", "Detailing", "Car Wash"],
    "Personal Care": ["Massage", "Haircut", "Gym"]
}

def update_subtypes(index):
    category = type_combo.currentText()
    subtype_combo.clear()
    if category and category in sub_options:
        subtype_combo.addItems(sub_options[category])

def update_distance(val):
    distance_label.setText(f"Maximum Distance: {val} km")

# Add a results text area below the map
results_text = QTextEdit()
results_text.setReadOnly(True)
results_text.setMinimumHeight(150)
results_text.setVisible(False)  # Hide initially

# Modify your layout
map_layout = QVBoxLayout()
map_layout.addWidget(map_view)
map_layout.addWidget(results_text)

main_layout.addWidget(scroll_area, 2)
main_layout.addLayout(map_layout, 3)

def run_search():
    category = type_combo.currentText()
    subtype = subtype_combo.currentText()
    rating = selected_rating[0]
    distance_km = distance_slider.value()
    price_min = price_min_combo.currentIndex()
    price_max = price_max_combo.currentIndex()
    address = address_box.toPlainText()

    # Map UI category to actual place type
    place_types = {
        "Restaurants": "restaurant",
        "Hotels": "lodging",
        "Auto Services": "car_repair",
        "Personal Care": "spa"
    }
    place_type = place_types.get(category, None)
    if not place_type:
        print("Invalid or unselected service type.")
        return

    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            lat, lng = location['lat'], location['lng']

            places_result = gmaps.places_nearby(
                location=(lat, lng),
                radius=distance_km * 1000,
                type=place_type,
                keyword=subtype
            )

            if places_result['results']:
                random_place = random.choice(places_result['results'])
                rand_lat = random_place['geometry']['location']['lat']
                rand_lng = random_place['geometry']['location']['lng']

                # Display place info in the results text area
                place_info = f"""
                <h2>📍 {random_place.get('name', 'N/A')}</h2>
                <p><b>📌 Address:</b> {random_place.get('vicinity', 'N/A')}</p>
                <p><b>⭐ Rating:</b> {random_place.get('rating', 'N/A')}/5</p>
                <p><b>💰 Price Level:</b> {"$" * random_place.get('price_level', 0) or 'N/A'}</p>
                <p><b>🔖 Types:</b> {', '.join(random_place.get('types', []))}</p>
                """
                
                results_text.setHtml(place_info)
                results_text.setVisible(True)

                # Update map
                map_url = f"https://www.openstreetmap.org/?mlat={rand_lat}&mlon={rand_lng}#map=15/{rand_lat}/{rand_lng}"
                map_view.setUrl(QUrl(map_url))
            else:
                results_text.setHtml("<p>No places found matching your criteria.</p>")
                results_text.setVisible(True)
                print("No places found matching the criteria.")

    except Exception as e:
        results_text.setHtml(f"<p>Error during search: {str(e)}</p>")
        results_text.setVisible(True)
        print(f"Error during search: {str(e)}")

type_combo.currentIndexChanged.connect(update_subtypes)
distance_slider.valueChanged.connect(update_distance)
search_button.clicked.connect(run_search)

# ----------- SHOW -----------
window.showMaximized()
sys.exit(app.exec())
