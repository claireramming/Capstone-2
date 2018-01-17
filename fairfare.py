from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators, StringField, SubmitField, IntegerField, SelectField
import numpy as np
import dill as pickle

#import pickled files
filename = 'pickled/model_v1.pk'
with open(filename ,'rb') as f:
    loaded_model = pickle.load(f)

filename = 'pickled/sorted_arrays.pk'
with open(filename ,'rb') as f:
    sorted_arrays = pickle.load(f)
    
filename = 'pickled/feature_arrays.pk'
with open(filename ,'rb') as f:
    feature_arrays = pickle.load(f)

#initialize objects from pickled files

#sorted arrays
properties = sorted_arrays[0]
neighbs = sorted_arrays[1]
rooms = sorted_arrays[2]
bors = sorted_arrays[3]

#feature arrays
property_types = feature_arrays[0]
neighborhoods = feature_arrays[1]
boroughs = feature_arrays[2]
room_types = feature_arrays[3]

#define functions

def set_property(prop_in):
    props = np.searchsorted(properties, prop_in)

    if props != 0:
        for i in range(10):
            property_types[i][props-1] = 1
        
def set_neighborhood(neighb_in):
    neighb = np.searchsorted(neighbs, neighb_in)

    if neighb != 0:
        for i in range(10):
            neighborhoods[i][neighb-1] = 1
        
def set_borough(borough_in):
    bor = np.searchsorted(bors, borough_in)

    if bor != 0:
        for i in range(10):
            boroughs[i][bor-1] = 1

def set_room(room_in):
    room = np.searchsorted(rooms, room_in)

    if room != 0:
        for i in range(10):
            room_types[i][room-1] = 1

def build_numerical(beds_in, accom_in):
    array = np.zeros((10,4))
    for i in range(10):
        array[i][3] = int(accom_in) #accomodates
        array[i][2] = int(beds_in) #num of beds
        array[i][1] = (np.random.rand() * 2) + 3 #rating - generate a number between 3 and 5
        array[i][0] = np.random.randint(1, 454) #num of reviews, generate number between 1 and max # of reviews
    return array

def predict_price(prop, neighb, borough, room, room_num, accom_num):   
    set_property(prop)
    set_neighborhood(neighb)
    set_borough(borough)
    set_room(room)
    numerical = build_numerical(room_num,accom_num)

    features = np.concatenate((numerical, room_types, boroughs, neighborhoods, property_types), 1)
    y_pred = loaded_model.predict(features)
    average = np.mean(y_pred).round(0)
    return average


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    prop_type = SelectField(u'Prop Type:', choices=[('Apartment', 'Apartment'), ('Bed & Breakfast', 'Bed & Breakfast'), ('Loft', 'Loft'), ('Townhouse', 'Townhouse'), ('Condominium', 'Condominium'), ('House','House'), ('Other', 'Other')], validators=[validators.required()])
    num_rooms = IntegerField('# Bedrooms:', validators=[validators.required()])
    num_accom = IntegerField('# Accomodates:', validators=[validators.required()])
    room_type = SelectField(u'Room Type:', choices=[('Shared room', 'Shared room'), ('Entire home/apt', 'Entire home/apt'), ('Private room', 'Private room')], validators=[validators.required()])
    borough = SelectField(u'Borough:', choices=[('Manhattan', 'Manhattan'), ('Brooklyn', 'Brooklyn'), ('Bronx', 'Bronx'), ('Queens', 'Queens'), ('Staten Island', 'Staten Island')], validators=[validators.required()])
    neighborhood = SelectField(u'Neighborhood:', choices=[('Jackson Heights', 'Jackson Heights'),('Cypress Hills', 'Cypress Hills'),('Sheepshead Bay', 'Sheepshead Bay'),("Hell's Kitchen", "Hell's Kitchen"),('Harlem', 'Harlem'),('Theater District', 'Theater District'),('East Village', 'East Village'),('St. Albans', 'St. Albans'),('East Harlem', 'East Harlem'),('Arverne', 'Arverne'), \
                                                          ('Upper West Side', 'Upper West Side'),('Washington Heights', 'Washington Heights'), ('Long Island City', 'Long Island City'), ('Financial District', 'Financial District'),('Upper East Side', 'Upper East Side'), ('Midtown', 'Midtown'), ('Kips Bay', 'Kips Bay'),('Gramercy', 'Gramercy'),('Astoria', 'Astoria'),('Lower East Side', 'Lower East Side'), \
                                                          ('Chelsea', 'Chelsea'),('Woodside', 'Woodside'),('Bushwick', 'Bushwick'),('Williamsburg', 'Williamsburg'), ('West Village', 'West Village'),('Boerum Hill', 'Boerum Hill'), ('Sunset Park', 'Sunset Park'), ('Fort Greene', 'Fort Greene'), ('Greenwich Village', 'Greenwich Village'), ('Prospect Heights', 'Prospect Heights'), \
                                                          ('Morningside Heights', 'Morningside Heights'),('Park Slope', 'Park Slope'),('Nolita', 'Nolita'), ('Flatlands', 'Flatlands'), ('Brighton Beach', 'Brighton Beach'), ('Canarsie', 'Canarsie'), ('Rockaway Beach', 'Rockaway Beach'), ('Fort Hamilton', 'Fort Hamilton'), ('Crown Heights', 'Crown Heights'), ('Flatbush', 'Flatbush'), \
                                                          ('Murray Hill', 'Murray Hill'), ('Inwood', 'Inwood'), ('Norwood', 'Norwood'), ('Corona', 'Corona'), ('Bedford-Stuyvesant', 'Bedford-Stuyvesant'), ('Flushing', 'Flushing'), ('Jamaica', 'Jamaica'), ('Mott Haven', 'Mott Haven'), ('East Flatbush', 'East Flatbush'), ('Little Italy', 'Little Italy'), ('Flatiron District', 'Flatiron District'), \
                                                          ('Clinton Hill', 'Clinton Hill'),('Forest Hills', 'Forest Hills'),('East Elmhurst', 'East Elmhurst'), ('Greenpoint', 'Greenpoint'), ('Prospect-Lefferts Gardens', 'Prospect-Lefferts Gardens'), ('SoHo', 'SoHo'), ('Downtown Brooklyn', 'Downtown Brooklyn'),('Battery Park City', 'Battery Park City'), ('Concourse Village', 'Concourse Village'), \
                                                          ('Roosevelt Island', 'Roosevelt Island'), ('Shore Acres', 'Shore Acres'), ('Midwood', 'Midwood'), ('Borough Park', 'Borough Park'), ('Kensington', 'Kensington'), ('Maspeth', 'Maspeth'), ('Elmhurst', 'Elmhurst'),('Ditmars Steinway', 'Ditmars Steinway'),('Woodhaven', 'Woodhaven'), ('Marble Hill', 'Marble Hill'), ('Ridgewood', 'Ridgewood'), \
                                                          ('Rego Park', 'Rego Park'), ('Kew Gardens', 'Kew Gardens'),('Sunnyside', 'Sunnyside'), ('Brownsville', 'Brownsville'), ('Parkchester', 'Parkchester'),('Bronxdale', 'Bronxdale'), ('Riverdale', 'Riverdale'), ('Kingsbridge', 'Kingsbridge'), ('Queens Village', 'Queens Village'), ('Far Rockaway', 'Far Rockaway'), ('Middle Village', 'Middle Village'), \
                                                          ('Concourse', 'Concourse'), ('Gowanus', 'Gowanus'), ('Bensonhurst', 'Bensonhurst'), ('Gravesend', 'Gravesend'),('Windsor Terrace', 'Windsor Terrace'),('Chinatown', 'Chinatown'), ('Clason Point', 'Clason Point'), ('Coney Island', 'Coney Island'), ('East New York', 'East New York'), ('Cambria Heights', 'Cambria Heights'), ('NoHo', 'NoHo'), \
                                                          ('Rockaway Park', 'Rockaway Park'), ('Spuyten Duyvil', 'Spuyten Duyvil'), ('Schuylerville', 'Schuylerville'), ('Mount Eden', 'Mount Eden'),('Springfield Gardens', 'Springfield Gardens'), ('Rosedale', 'Rosedale'), ('Richmond Hill', 'Richmond Hill'), ('Todt Hill', 'Todt Hill'), ('Jamaica Estates', 'Jamaica Estates'), ('Two Bridges', 'Two Bridges'), \
                                                          ('Cobble Hill', 'Cobble Hill'), ('South Slope', 'South Slope'), ('Carroll Gardens', 'Carroll Gardens'), ('Red Hook', 'Red Hook'), ('Tribeca', 'Tribeca'), ('Central Park', 'Central Park'), ('Forest Park', 'Forest Park'), ('Fresh Meadows', 'Fresh Meadows'), ('College Point', 'College Point'), ('Stuyvesant Town', 'Stuyvesant Town'), \
                                                          ('Tottenville', 'Tottenville'), ('South Beach', 'South Beach'), ('Civic Center', 'Civic Center'), ('Brooklyn Heights', 'Brooklyn Heights'), ('Belle Harbor', 'Belle Harbor'), ('Whitestone', 'Whitestone'), ('Neponsit', 'Neponsit'), ('St. George', 'St. George'), ('Graniteville', 'Graniteville'), ('Arrochar', 'Arrochar'), ('DUMBO', 'DUMBO'), \
                                                          ('Vinegar Hill', 'Vinegar Hill'), ('Columbia St', 'Columbia St'), ('Bergen Beach', 'Bergen Beach'), ('Navy Yard', 'Navy Yard'), ('Bayside', 'Bayside'), ('Mount Hope', 'Mount Hope'), ('Stapleton', 'Stapleton'), ('Howard Beach', 'Howard Beach'), ('Bay Ridge', 'Bay Ridge'), ('Lighthouse Hill', 'Lighthouse Hill'), ('Mariners Harbor', 'Mariners Harbor'), \
                                                          ('Randall Manor', 'Randall Manor'),('Wakefield', 'Wakefield'), ('Tompkinsville', 'Tompkinsville'), ('Bath Beach', 'Bath Beach'), ('Dyker Heights', 'Dyker Heights'), ('Prospect Park', 'Prospect Park'),('Dongan Hills', 'Dongan Hills'), ('South Ozone Park', 'South Ozone Park'), ('Kew Gardens Hills', 'Kew Gardens Hills'), ('Laurelton', 'Laurelton'), \
                                                           ('Port Morris', 'Port Morris'), ('Melrose', 'Melrose'), ('Eastchester', 'Eastchester'),('Pelham Gardens', 'Pelham Gardens'), ('Manhattan Beach', 'Manhattan Beach'), ('Concord', 'Concord'), ('Park Hill', 'Park Hill'), ('Marine Park', 'Marine Park'), ('Fordham', 'Fordham'), ('Bellerose', 'Bellerose'), ('Jamaica Hills', 'Jamaica Hills'), \
                                                           ('Pelham Bay', 'Pelham Bay'), ('Allerton', 'Allerton'), ('City Island', 'City Island'), ('Huguenot', 'Huguenot'), ('Bay Terrace', 'Bay Terrace'), ('Claremont Village', 'Claremont Village'), ('Midland Beach', 'Midland Beach'), ('Clifton', 'Clifton'), ('Glendale', 'Glendale'), ('Longwood', 'Longwood'), ('Unionport', 'Unionport'), \
                                                           ('East Morrisania', 'East Morrisania'), ('Latourette Park', 'Latourette Park'), ('Howland Hook', 'Howland Hook'),('Holliswood', 'Holliswood'), ('New Brighton', 'New Brighton'), ('Crotona Park', 'Crotona Park'), ('Highbridge', 'Highbridge'), ('Van Cortlandt Park', 'Van Cortlandt Park'), ('Briarwood', 'Briarwood'), ('Ozone Park', 'Ozone Park'), \
                                                          ('Silver Lake', 'Silver Lake'), ('West Brighton', 'West Brighton'), ('Fieldston', 'Fieldston'), ('Woodlawn', 'Woodlawn'), ('Williamsbridge', 'Williamsbridge'), ('Castle Hill', 'Castle Hill'),('Throgs Neck', 'Throgs Neck'), ('Great Kills', 'Great Kills'), ('Richmondtown', 'Richmondtown'), ('Grant City', 'Grant City'), ('Castleton Corners', 'Castleton Corners'), \
                                                          ('Bronx Park', 'Bronx Park'), ('Soundview', 'Soundview'),('Baychester', 'Baychester'),('Emerson Hill', 'Emerson Hill'),('Eltingville', 'Eltingville'),('University Heights', 'University Heights'), ('Hollis Hills', 'Hollis Hills'), ('Sea Gate', 'Sea Gate'),('Bayswater', 'Bayswater'), ('Belmont', 'Belmont'),('Edenwald', 'Edenwald'),('Glen Oaks', 'Glen Oaks'), \
                                                          ('Green-Wood Cemetery', 'Green-Wood Cemetery'), ('Port Richmond', 'Port Richmond'), ('LaGuardia Airport', 'LaGuardia Airport'), ('Hunts Point', 'Hunts Point'), ("Randall's Island", "Randall's Island"), ('North Riverdale', 'North Riverdale'), ('Douglaston', 'Douglaston'), ('Arden Heights', 'Arden Heights'), ('New Springville', 'New Springville'), \
                                                           ('Edgemere', 'Edgemere'), ('Grymes Hill', 'Grymes Hill'), ('Flushing Meadows Corona Park', 'Flushing Meadows Corona Park'), ('Hollis', 'Hollis'), ('Morris Heights', 'Morris Heights'), ('Westchester Square', 'Westchester Square'), ('Morrisania', 'Morrisania'), ('Co-op City', 'Co-op City'), ('Tremont', 'Tremont'), ('Van Nest', 'Van Nest'), ('West Farms', 'West Farms')])
 
 
@app.route("/", methods=['GET', 'POST'])
def fillform():
    form = ReusableForm(request.form)
 
    print(form.errors)
    if request.method == 'POST':
        prop_type=request.form['prop_type']
        num_rooms=request.form['num_rooms']
        num_accom=request.form['num_accom']
        room_type=request.form['room_type']
        borough=request.form['borough']
        neighborhood=request.form['neighborhood']
        print(prop_type, num_rooms, num_accom, room_type, borough, neighborhood)
 
        if form.validate():
            # Save the comment here.
            num = predict_price(prop_type, neighborhood, borough, room_type, num_rooms, num_accom)
            flash('suggested fare: $' + str(num) + '0')
            
            #flash('Looking for a ' + room_type + ' in a ' + prop_type + ' with ' + num_rooms + ' bedrooms ' + ' that accomodates ' + num_accom + ' in the ' + neighborhood + ' neighborhood of '+ borough)
        else:
            flash('All the form fields are required. ')
 
    return render_template('fillform.html', form=form)
 
if __name__ == "__main__":
    app.run()